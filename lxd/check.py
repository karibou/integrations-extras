import time
import requests
import requests_unixsocket
import urllib

from checks import AgentCheck
from hashlib import md5


class LXDCheck(AgentCheck):
    lxd_api = None
    statistics = {}
    baseURL = 'http+unix://' + urllib.quote_plus('/var/lib/lxd/unix.socket')
    containers = '/1.0/containers'
    stats = '/1.0/containers/%s/state'

    def check(self, instance):
        pass

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
                'msg_text': 'Unable to connect to LXD daemon : %s' %e
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

    def get_container_statistics(self, container):
        if container:
            self.statistics[container] = self._query_lxd(self.stats % container)
            return self.statistics

if __name__ == '__main__':
    check, instances = LXDCheck.from_yaml('/etc/dd-agent/conf.d/lxd.yaml')
    containers = check.get_containers()
    if containers:
        check.gauge('lxd.containers', containers, tags=['containers'])
