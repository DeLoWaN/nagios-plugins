# nagios-plugins
Collection of different nagios plugins

## Check Elasticsearch
I've created this check since I didn't find a check which was compatible with Elasticsearch 5.1 with authentication in HTTPS. This check was tested against [Elastic Cloud](https://cloud.elastic.co/) by Elastic.co.

Features:
- Check the status of an Elasticsearch cluster (Green/Yellow/Red) with metrics.
- Check the cpu / java heap memory / filesystem usage percentage of a particular node on the cluster when providing the *--node* switch.

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

## Check Elasticsearch last entry

Checks the last entry on an index (wildcard may be used). Basically it make a ES query on your index with

```json
{
  "query": {
    "match_all": {}
  },
  "size": 1,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
```

You can customize the search with the *--query* parameter. It will replace the *match_all* term. For example, with `-q '{"term":{"host":"example.com"}}'`, it will use this query :

```json
{
  "query": {
    "term": {
      "host": "example.com"
    }
  },
  "size": 1,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
```

```
usage: check_elasticsearch_last_entry.py [-h] -H ELASTICSEARCH_HOST
                                         [-P ELASTICSEARCH_PORT] [-s]
                                         [-i INDEX] [-q QUERY] [-w WARNING]
                                         [-c CRITICAL] [-u USER] [-p PASSWORD]
                                         [-v]

Check the last entry of an index. Can be wildcarded. Returns ok if last entry
is fresh (customisable)

optional arguments:
  -h, --help            show this help message and exit
  -H ELASTICSEARCH_HOST, --host ELASTICSEARCH_HOST
                        The Elasticsearch host
  -P ELASTICSEARCH_PORT, --port ELASTICSEARCH_PORT
                        The Elasticsearch port
  -s, --ssl             Use this when connecting via SSL
  -i INDEX, --index INDEX
                        The index to check. Can be wildcarded
  -q QUERY, --query QUERY
                        Customise the query. Must be an ES json query string
  -w WARNING, --warning WARNING
                        Minimum difference in seconds from now to consider a
                        warning data missing. Defaults to 600.
  -c CRITICAL, --critical CRITICAL
                        Minimum difference in seconds from now to consider a
                        critical data missing. Defaults to 3600.
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  -v, --verbose
```