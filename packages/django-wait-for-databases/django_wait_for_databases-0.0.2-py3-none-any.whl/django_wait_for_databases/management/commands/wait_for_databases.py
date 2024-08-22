import asyncio
import logging
from typing import Any

from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand, CommandParser
from django.db import OperationalError, connections

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Wait for database connections."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--timeout",
            default=30,
            type=int,
            help="How long to wait before an error is thrown",
        )

        parser.add_argument(
            "--interval",
            default=2,
            type=int,
            help="Interval between checks for the database connections.",
        )

    def handle(self, *args: Any, **options: Any):
        timeout = options["timeout"]
        interval = options["interval"]
        try:
            async_to_sync(asyncio.wait_for)(
                self.wait_for_connections(interval=interval), timeout=timeout
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "SUCCESS: All databases connections have been established"
                )
            )
        except asyncio.exceptions.TimeoutError:
            self.stderr.write(
                self.style.ERROR(
                    "TIMEOUT: Couldn't establish connection to all databases"
                )
            )
            raise CommandError(
                "TIMEOUT: Couldn't establish connection to all databases"
            )

    async def wait_for_connections(self, interval: int):
        databases = settings.DATABASES.keys()
        logger.debug("Connecting to %s", ", ".join(databases))
        while True:
            results = await asyncio.gather(
                *[
                    sync_to_async(self.check_connection)(database)
                    for database in databases
                ]
            )
            if all(results):
                return
            await asyncio.sleep(interval)

    def check_connection(self, database: str):
        try:
            with connections[database].cursor():
                self.stdout.write(
                    self.style.SUCCESS(
                        "Connection established to database %s" % database
                    )
                )
                return True
        except OperationalError as e:
            self.stderr.write(
                self.style.WARNING("Cannot connect to database %s: %s" % (database, e))
            )
            return False
