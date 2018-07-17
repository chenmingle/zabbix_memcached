# 使用python监控memcached基本信息

  

## 使用python监控memcached的基本信息，例如：connections、hitRate、freeMemory、memoryUsage、evictions等等。然后自定义zabbix keys值实现自定义监控模版！


### 首先安装需要的环境：

```
pip install python-memcached
```

### 话不多说，直接上脚本：
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenmingle'

import sys
import subprocess
import json

try:
    import memcache
except Exception, e:
    print 'pip install python-memcached'
    sys.exit(1)


class Memcached(object):
    def __init__(self, host_list):
        self.mc = memcache.Client(host_list)
        try:
            self.stats = self.mc.get_stats()[0][1]
        except Exception, e:
            pass

    def get_curr_connections(self):
        """
        Get current connections for Memcached
        UserParameter: connections
        """
        try:
            return int(self.stats['curr_connections'])
        except Exception, e:
            return 0

    def get_cache_hit_rate(self):
        """
        Get the hit rate for Memcached
        UserParameter: hitRate
        """
        try:
            rate = float(self.stats['get_hits']) / float(self.stats['cmd_get'])
            return "%.2f" % (rate * 100)
        except Exception, e:
            return 0.0

    def get_free_memory(self):
        """
        Get the free memory in Memcached Byte
        UserParameter: freeMemory
        """
        try:
            free = int(self.stats['limit_maxbytes']) - int(self.stats['bytes'])
            return free
        except Exception, e:
            return 0

    def get_memory_usage_rate(self):
        """
        Get the memory usage rate in Memcached
        UserParameter: memoryRate
        """
        try:
            rate = float(self.stats['bytes']) / float(self.stats['limit_maxbytes'])
            return "%.2f" % (rate * 100)
        except Exception, e:
            return 0.0

    def get_evictions(self):
        """
        Get evictd items in Memcached one minute avg
        UserParameter: evictions
        """
        try:
            # minutes = int(self.stats['uptime']) / 60
            # return int(self.stats['evictions']) / int(minutes)
            return int(self.stats['evictions'])
        except Exception, e:
            return 0

    def test(self):
        # print json.dumps(self.stats, indent=4)
        print 'connections: %s' % self.get_curr_connections()
        print 'hitRate: %s %%' % self.get_cache_hit_rate()
        print 'freeMemory: %s Byte' % self.get_free_memory()
        print 'memoryUsage: %s %%' % self.get_memory_usage_rate()
        print 'evictions: %s' % self.get_evictions()
        print 'alive: %s' % check_alive(host_list)


def check_alive(host_list):
    host = host_list.split(':')[0]
    port = host_list.split(':')[1]
    cmd = 'nc -z %s %s > /dev/null 2>&1' % (host, port)
    return subprocess.call(cmd, shell=True)


def parse(type, host_list):
    mc = Memcached([host_list])
    if type == 'connections':
        print mc.get_curr_connections()
    elif type == 'hitRate':
        print mc.get_cache_hit_rate()
    elif type == 'freeMemory':
        print mc.get_free_memory()
    elif type == 'memoryUsage':
        print mc.get_memory_usage_rate()
    elif type == 'evictions':
        print mc.get_evictions()
    elif type == 'alive':
        print check_alive(host_list)
    else:
        mc.test()

if __name__ == '__main__':
    try:
        host_list = sys.argv[1]
        type = sys.argv[2]
    except Exception, e:
        print "Usage: python %s 127.0.0.1:11211 connections" % sys.argv[0]
        sys.exit(1)
    parse(type, host_list)
```

### 例行测试一下脚本的效果：
```
[root@Memcached zabbix_agentd.d]# /usr/local/bin/python /home/python/check_memcached.py 10.0.0.90:11211 test
connections: 1593
hitRate: 98.15 %
freeMemory: 849551027 Byte
memoryUsage: 80.22 %
evictions: 7477932
alive: 0
```
### 现在已经完成一个简单的监控memcached基本信息的脚本了，接下来为了以后方便查看做个自定义监控项加入到zabbix上去。

* 首先定义监控项配置：

```
cd /etc/zabbix/zabbix_agentd.d
cat Memcached.conf
# Memcached
UserParameter=memcached.stats[*],/usr/local/bin/python /home/python/check_memcached.py 10.0.0.90:11211 $1
```
* 在zabbix上配置自定义模版自定义监控项：





