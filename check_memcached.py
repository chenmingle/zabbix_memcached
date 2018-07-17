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
