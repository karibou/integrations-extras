# stdlib
from mock import patch
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest, load_check


@attr(requires='lxd')
class TestLxd(AgentCheckTest):
    """Basic Test for lxd integration."""
    CHECK_NAME = 'lxd'

    def __init__(self, *args, **kwargs):
        super(TestLxd, self).__init__(*args, **kwargs)

        self.config = {'init_config': [{'min_collection_interval': 300}]}
        self.config = {'instances': [{'excluded_ifaces': ['lo']}]}
        self.check = load_check(self.CHECK_NAME, self.config, {})

    LXD_API_DATA = [
        [u'/1.0/containers/MyContainer'],
        {
            u'processes': 15,
            u'network': {
                u'lo': {},
                u'eth0': {
                    u'counters': {
                        u'packets_sent': 8,
                        u'bytes_received': 270446,
                        u'bytes_sent': 648,
                        u'packets_received': 924
                    }
                }
            },
            u'memory': {
                u'usage': 53620735,
                u'swap_usage': 0,
                u'swap_usage_peak': 0,
                u'usage_peak': 124780544
            },
        },
        [u'/1.0/containers/MyContainer'],
        {
            u'processes': 15,
            u'network': {
                u'lo': {},
                u'eth0': {
                    u'counters': {
                        u'packets_sent': 12,
                        u'bytes_received': 270447,
                        u'bytes_sent': 650,
                        u'packets_received': 927
                    }
                }
            },
            u'memory': {
                u'usage': 53620735,
                u'swap_usage': 0,
                u'swap_usage_peak': 0,
                u'usage_peak': 124780544
            },
        }
    ]

    CX_STATE_GAUGES_VALUES = {
        'lxd.MyContainer.processes': 15,
        'lxd.MyContainer.memory.usage': 53620735,
        'lxd.MyContainer.memory.usage_peak': 124780544,
        'lxd.MyContainer.memory.swap_usage': 0,
        'lxd.MyContainer.memory.swap_usage_peak': 0,
        'lxd.MyContainer.net.bytes_rcvd': 1,
        'lxd.MyContainer.net.bytes_sent': 2,
        'lxd.MyContainer.net.packets_in': 3,
        'lxd.MyContainer.net.packets_out': 4,
    }

    @patch('_lxd.LXDCheck._query_lxd', side_effect=LXD_API_DATA)
    def test_lxd(self, mock_lxd_query):
        """
        Testing Lxd check.
        """

        # run your actual tests...
        # Needs to be run twice so rates are correctly updated
        self.run_check_twice({})

        # Assert metrics
        for metric, value in self.CX_STATE_GAUGES_VALUES.iteritems():
            self.assertMetric(metric, value=value)

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()
