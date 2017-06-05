# stdlib
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest




@attr(requires='lxd')
class TestLxd(AgentCheckTest):
    """Basic Test for lxd integration."""
    CHECK_NAME = 'lxd'

    def test_check(self):
        """
        Testing Lxd check.
        """
        self.load_check({}, {})

        # run your actual tests...

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
