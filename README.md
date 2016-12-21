# nagios-plugins
Collection of different nagios plugins

## Check Elasticsearch
- Check the status of an Elasticsearch cluster
- Check the cpu / java heap memory percentage of a particular node on the cluster

```
usage: check_elasticsearch.py [-h] -H ELASTICSEARCH_HOST
                              [-P ELASTICSEARCH_PORT] [-s] [-n NODE]
                              [-cw CPU_WARNING] [-hw HEAP_WARNING]
                              [-fw FS_WARNING] [-cc CPU_CRITICAL]
                              [-hc HEAP_CRITICAL] [-fc FS_CRITICAL] [-u USER]
                              [-p PASSWORD] [-v]

Check health of an Elasticsearch host. If --node is specified, check health of
the node instead.
optional arguments:
  -h, --help            show this help message and exit
  -H ELASTICSEARCH_HOST, --host ELASTICSEARCH_HOST
                        The Elasticsearch host
  -P ELASTICSEARCH_PORT, --port ELASTICSEARCH_PORT
                        The Elasticsearch port
  -s, --ssl             Use this when connecting via SSL
  -n NODE, --node NODE  Check health of a particular node
  -cw CPU_WARNING, --cpu-warning CPU_WARNING
                        Minimum value of CPU percentage to return a warning
                        state. Defaults to 90.
  -hw HEAP_WARNING, --heap-warning HEAP_WARNING
                        Minimum value of Java Heap size to return a warning
                        state. Defaults to 90.
  -fw FS_WARNING, --fs-warning FS_WARNING
                        Minimum value of file system size to return a warning
                        state. Defaults to 90.
  -cc CPU_CRITICAL, --cpu-critical CPU_CRITICAL
                        Minimum value of CPU percentage to return a critical
                        state. Defaults to 95.
  -hc HEAP_CRITICAL, --heap-critical HEAP_CRITICAL
                        Minimum value of Java Heap size to return a critical
                        state. Defaults to 95.
  -fc FS_CRITICAL, --fs-critical FS_CRITICAL
                        Minimum value of file system size to return a critical
                        state. Defaults to 95.
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  -v, --verbose
```
