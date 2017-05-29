import time
import requests
import requests_unixsocket
import urllib

from checks import AgentCheck


class LXDCheck(AgentCheck):
    lxd_api = None
    stats = {}
    baseURL = 'http+unix://' + urllib.quote_plus('/var/lib/lxd/unix.socket')
    containers = '/1.0/containers'
    state = '/1.0/containers/%s/state'
    m_metrics = {}
    net_metrics = {}

    def check(self, instance):
        containers = self.get_containers()
        for container in containers:
            self.get_container_statistics(container)
            self.send_processes_statistics(container)
            self.send_memory_statistics(container)
            self.send_network_statistics(container)

    def _connect_local_client(self):
        try:
            self.lxd_api = requests_unixsocket.Session()
            self.lxd_api.get('%s' % self.baseURL)
            return True
        except requests.exceptions.ConnectionError as e:
            self.log.debug('Unable to connect to LXD daemon : %s' % e)
            self.event({
                'timestamp': int(time.time()),
                'event_type': 'lxd_check',
                'msg_title': 'LXD CONN',
                'msg_text': 'Unable to connect to LXD daemon : %s' % e
            })
            return False

    def _query_lxd(self, data_element):
        if self.lxd_api is None:
            self._connect_local_client()

        lxd_data = self.lxd_api.get('%s%s' % (self.baseURL, data_element))
        if lxd_data.json()['status_code'] == 200:
            return lxd_data.json()['metadata']
        else:
            return None

    def get_containers(self):
        container_data = self._query_lxd(self.containers)
        self.container_list = [c.split('/')[-1] for c in container_data]
        return self.container_list

    def get_container_statistics(self, containr):
        if containr:
            self.stats[containr] = self._query_lxd(self.state % containr)
            return self.stats

    def send_processes_statistics(self, containr):
        self.gauge('lxd.%s.processes' % str(containr),
                   self.stats[containr]['processes'])

    def send_memory_statistics(self, containr):
            self.m_metrics = {
                'usage': 'usage',
                'usage_peak': 'usage_peak',
                'swap_usage': 'swap_usage',
                'swap_usage_peak': 'swap_usage_peak',
            }
            for metric in self.m_metrics.keys():
                self.gauge('lxd.%s.memory.%s' % (str(containr), metric),
                           self.stats[containr]['memory']
                                     [self.m_metrics[metric]])

    def send_network_statistics(self, containr):
            self.net_metrics = {
                'bytes_rcvd': 'bytes_received',
                'bytes_sent': 'bytes_sent',
                'packets_in': 'packets_received',
                'packets_out': 'packets_sent',
            }
            nics = self.stats[containr]['network'].keys()
            if 'excluded_ifaces' in self.instances[0].keys():
                for unwanted_nic in self.instances[0]['excluded_ifaces']:
                    nics.remove(unicode(unwanted_nic))
            for nic in nics:
                for metric in self.net_metrics.keys():
                    self.rate('lxd.%s.net.%s' % (str(containr), metric),
                              self.stats[containr]['network'][nic]['counters']
                              [self.net_metrics[metric]], device_name=nic)


if __name__ == '__main__':
    check, instances = LXDCheck.from_yaml('/etc/dd-agent/conf.d/lxd.yaml')
    containers = check.get_containers()
    if containers:
        for container in containers:
            check.get_container_statistics(container)
            check.send_processes_statistics(container)
            check.send_network_statistics(container)
