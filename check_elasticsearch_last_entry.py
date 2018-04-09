import requests
import json
import argparse
import traceback
import dateutil.parser
from datetime import datetime
from dateutil.tz import tzlocal

class AuthError(Exception):
    pass
class NoResultsError(Exception):
    pass
class ESError(Exception):
    pass

def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd, %dh%dm%ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)

parser = argparse.ArgumentParser(description='Check the last entry of an index. Can be wildcarded. Returns ok if last entry is fresh (customisable)')
parser.add_argument('-H', '--host', required=True, help='The Elasticsearch host', metavar='ELASTICSEARCH_HOST')
parser.add_argument('-P', '--port', help='The Elasticsearch port', metavar='ELASTICSEARCH_PORT', default='9200')
parser.add_argument('-s', '--ssl', action='store_true', help='Use this when connecting via SSL')
parser.add_argument('-i', '--index', help='The index to check. Can be wildcarded', default='_all')
parser.add_argument('-q', '--query', help='Customise the query. Must be an ES json query string', default='{"match_all": {}}')
parser.add_argument('-w', '--warning', type=int, default=600, help='Minimum difference in seconds from now to consider a warning data missing. Defaults to 600.')
parser.add_argument('-c', '--critical', type=int, default=3600, help='Minimum difference in seconds from now to consider a critical data missing. Defaults to 3600.')
parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-v', '--verbose', action='count')

args = parser.parse_args()

try:
    url = 'http{}://{}:{}/{}/_search'.format('s' if args.ssl else '', args.host, args.port if args.port is not None else '', args.index)

    query = '{"query":%s,"size":1,"sort":[{"@timestamp":{"order":"desc"}}]}' % (args.query)
    if args.user is None:
        response = requests.get(
            url,
            data=query,
            headers={'content-type': 'application/json'})
    else:
        response = requests.get(
        url,
        auth=requests.auth.HTTPBasicAuth(
            args.user,
            args.password),
        data=query,
        headers={'content-type': 'application/json'})

    if response.status_code == 401:
        raise AuthError('Authentication Error')
    res = json.loads(response.text)

    if 'error' in res:
        raise ESError('Elasticsearch Error')

    if res['hits']['total'] == 0:
        raise NoResultsError('No Results Error')
    
    lastdata = dateutil.parser.parse(res['hits']['hits'][0]['_source']['@timestamp'])
    diff = datetime.now(tzlocal()) - lastdata
    index = res['hits']['hits'][0]['_index']
    print('Index {} last fetch data was at {} ({} ago)'.format(index, lastdata.strftime("%Y-%m-%d %H:%M:%S"), pretty_time_delta(diff.total_seconds())))
    print('|difference_in_seconds={}.'.format(round(diff.total_seconds())))
    if diff.total_seconds() > args.critical:
        exit(2)
    elif diff.total_seconds() > args.warning:
        exit(1)
    else:
        exit(0)

except AuthError:
    print('ES returns 401: Unauthorized. Check login/password.')
    if args.verbose: traceback.print_exc()
except ESError:
    print('ES didn\'t really like your query. Retry with a different one')
    print('type: {}'.format(res['error']['type']))
    print('reason: {}'.format(res['error']['reason']))
    if args.verbose: traceback.print_exc()
except NoResultsError:
    print('ES returns no results. Check your query.')
    if args.verbose: traceback.print_exc()
except requests.exceptions.ConnectionError:
    print('Failed to connect to ES Host. Check URL or protocol used.')
    if args.verbose: traceback.print_exc()
except Exception:
    print('Error connecting to ES Host. Check parameters.')
    if args.verbose: traceback.print_exc()
    print(url)
    exit(3)
