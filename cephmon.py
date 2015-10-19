# coding=utf-8

"""
The CephMonCollector collects utilization info from Ceph monitors

#### Dependencies

 * ceph [http://ceph.com/]
 * librados (python) [http://docs.ceph.com/docs/master/rados/api/python/]

"""

try:
    import json
except ImportError:
    import simplejson as json

try:
    from rados import Rados
except ImportError:
    Rados = None

import diamond.collector


class CephClusterCommand(dict):
    """
    Issue a ceph command on the given cluster and provide the returned json
    """

    def __init__(self, cluster, **kwargs):
        dict.__init__(self)
        ret, buf, err = cluster.mon_command(json.dumps(kwargs), '', timeout=5)
        if ret != 0:
            self['err'] = err
        else:
            self.update(json.loads(buf))


class CephMonCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(CephMonCollector, self).get_default_config_help()
        config_help.update({
            'ceph_config': 'The location of the ceph.conf'
                           ' Defaults to "/etc/ceph/ceph.conf"',
            'client_name': 'Client name to use for connecting to ceph'
                             ' Defaults to "client.admin"',
            'keyrinf': 'Path to the keyring to use for connecting'
                          ' Defaults to "/etc/ceph/keyring"',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CephMonCollector, self).get_default_config()
        config.update({
            'path': 'ceph',
            'ceph_config': '/etc/ceph/ceph.conf',
            'client_name': 'client.admin',
            'keyring': '/etc/ceph/keyring',
        })
        return config

    def collect(self):
        """
        Collect stats from ceph monitors via librados
        """

        if Rados is None:
            self.log.error('Unable to import module Rados')
            return {}

        perf_values = ['bytes_used', 'bytes_total', 'bytes_avail',
                       'data_bytes', 'num_pgs', 'op_per_sec',
                       'read_bytes_sec', 'write_bytes_sec', 'pgs_by_state',
                       'osdmap']

        cluster_conf = dict(
            conffile = self.config['ceph_config'],
            conf = dict(keyring=self.config['keyring']),
            name=self.config['client_name']
        )

        with Rados(**cluster_conf) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='status', format='json')
            if 'err' in cluster_status:
                self.log.error('Unable to get cluster status: ' + cluster_status['err'])

            for value in perf_values:
                if value == 'osdmap':
                    for key, value in cluster_status['osdmap']['osdmap'].iteritems():
                        self.publish('osdstats.' + key, int(value))
                elif value == 'pgs_by_state':
                    for state in cluster_status['pgmap'][value]:
                        self.publish('pgstats.' + state['state_name'], state['count'])
                else:
                    self.publish('cluster.' + value, cluster_status['pgmap'].get(value, 0))
