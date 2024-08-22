from io import StringIO
from unittest import TestCase

from django.core.management import call_command


class WaitForDatabaseSuccessTestCase(TestCase):
    def test_management_command_success(self):
        out = StringIO()
        result = call_command("wait_for_databases", timeout=5, stdout=out)
        self.assertIn("SUCCESS", out.getvalue(), msg=result)
