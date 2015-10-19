# Diamond collector for gather ceph cluster overall statistics

I am aware that there are already two collectors for ceph in [Diamonds](https://github.com/python-diamond/Diamond/) upstream repository. Anyways, one is just not working and the other one is not doing what I want. This one requires the python bindings for Librados and directly connects to the ceph cluster and gather the cluster overall statistics. No forking, no external programms required.

Collects the following metrics:

```
Metric: servers.ceph-mon-bs01.ceph.cluster.bytes_used
Metric: servers.ceph-mon-bs01.ceph.cluster.bytes_total
Metric: servers.ceph-mon-bs01.ceph.cluster.bytes_avail
Metric: servers.ceph-mon-bs01.ceph.cluster.data_bytes
Metric: servers.ceph-mon-bs01.ceph.cluster.num_pgs
Metric: servers.ceph-mon-bs01.ceph.cluster.op_per_sec
Metric: servers.ceph-mon-bs01.ceph.cluster.read_bytes_sec
Metric: servers.ceph-mon-bs01.ceph.cluster.write_bytes_sec
Metric: servers.ceph-mon-bs01.ceph.pgstats.active+clean
Metric: servers.ceph-mon-bs01.ceph.osdstats.full
Metric: servers.ceph-mon-bs01.ceph.osdstats.nearfull
Metric: servers.ceph-mon-bs01.ceph.osdstats.num_osds
Metric: servers.ceph-mon-bs01.ceph.osdstats.num_up_osds
Metric: servers.ceph-mon-bs01.ceph.osdstats.epoch
Metric: servers.ceph-mon-bs01.ceph.osdstats.num_in_osds

```
