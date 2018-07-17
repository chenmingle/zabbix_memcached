# 使用python监控memcached基本信息

  

## 使用python监控memcached的基本信息，例如：connections、hitRate、freeMemory、memoryUsage、evictions等等。然后自定义zabbix keys值实现自定义监控模版！


### 首先安装需要的环境：

```
pip install python-memcached
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





