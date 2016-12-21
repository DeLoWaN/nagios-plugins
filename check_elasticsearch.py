import requests
import json
import argparse
import traceback

class AuthError(Exception):
    pass

parser = argparse.ArgumentParser(description='Check health of an Elasticsearch host. If --node is specified, check health of the node instead.')
parser.add_argument('-H', '--host', required=True, help='The Elasticsearch host', metavar='ELASTICSEARCH_HOST')
parser.add_argument('-P', '--port', help='The Elasticsearch port', metavar='ELASTICSEARCH_PORT', default='9200')
parser.add_argument('-s', '--ssl', action='store_true', help='Use this when connecting via SSL')
parser.add_argument('-n', '--node', help='Check health of a particular node')
parser.add_argument('-cw', '--cpu-warning', type=int, default=90, help='Minimum value of CPU percentage to return a warning state. Defaults to 90.')
parser.add_argument('-hw', '--heap-warning', type=int, default=90, help='Minimum value of Java Heap size to return a warning state. Defaults to 90.')
parser.add_argument('-fw', '--fs-warning', type=int, default=90, help='Minimum value of file system size to return a warning state. Defaults to 90.')
parser.add_argument('-cc', '--cpu-critical', type=int, default=95, help='Minimum value of CPU percentage to return a critical state. Defaults to 95.')
parser.add_argument('-hc', '--heap-critical', type=int, default=95, help='Minimum value of Java Heap size to return a critical state. Defaults to 95.')
parser.add_argument('-fc', '--fs-critical', type=int, default=95, help='Minimum value of file system size to return a critical state. Defaults to 95.')
parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-v', '--verbose', action='count')

args = parser.parse_args()

eshost = 'http' + ('s' if args.ssl else '') + '://'+ args.host + (':' + args.port if args.port is not None else '')

try:
    if args.node is None:
        url = eshost + '/_cluster/health'
    else:
        url = eshost + '/_nodes/stats'

    if args.user is None:
        response = requests.get(
            url)
    else:
        response = requests.get(
        url,
        auth=requests.auth.HTTPBasicAuth(
            args.user,
            args.password))

    if response.status_code == 401:
        raise AuthError('Authentication Error')
    res = json.loads(response.text)
    
    if args.node is None:
        active_primary_shards = res['active_primary_shards']
        active_shards = res['active_shards']
        unassigned_shards = res['unassigned_shards']
        status = res['status']
        print('ES is {}'.format(status))
        print('|active_primary_shards={} active_shards={} unassigned_shards={}'.format(active_primary_shards, active_shards, unassigned_shards))
        if status == 'red':
            exit(2)
        elif status == 'yellow':
            exit(1)
        elif status == 'green':
            exit(0)
    else:
        cpu_usage = res['nodes'][args.node]['os']['cpu']['percent']
        jvm_heap_usage = res['nodes'][args.node]['jvm']['mem']['heap_used_percent']
        fs_usage = round(100 - 100 * res['nodes'][args.node]['fs']['total']['available_in_bytes'] / res['nodes'][args.node]['fs']['total']['total_in_bytes'])
        status=0
        if cpu_usage > args.cpu_critical:
            print('CPU is critical.', end='')
            status=2
        if jvm_heap_usage > args.heap_critical:
            print('Java Heap is critical.', end='')
            status=2
        if fs_usage > args.fs_critical:
            print('FS is critical.', end='')
            status=2
        if not status == 2:
            if cpu_usage > args.cpu_warning:
                print('CPU is warning.', end='')
                status=1
            if jvm_heap_usage > args.heap_warning:
                print('Java Heap is warning.', end='')
                status=1
            if fs_usage > args.fs_warning:
                print('FS is warning.', end='')
                status=1
        if status == 0:
            print('CPU, Java Heap and FS are ok.')
        else:
            print()
        print('|cpu_usage={} jvm_heap_usage={} fs_usage={}'.format(cpu_usage, jvm_heap_usage, fs_usage))
        exit(status)
    exit(0)

except AuthError:
    print('ES returns 401: Unauthorized. Check login/password.')
    if args.verbose: traceback.print_exc()
except requests.exceptions.ConnectionError:
    print('Failed to connect to ES Host. Check URL or protocol used.')
    if args.verbose: traceback.print_exc()
except Exception:
    print('Error connecting to ES Host. Check parameters.')
    if args.verbose: traceback.print_exc()
    print(eshost)
    exit(3)
