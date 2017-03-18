import argparse
from pprint import pprint

import requests


def main(email, password):
    path = 'http://localhost:4545'
    response = requests.get(path + '/').json()
    pprint(response)
    data = dict(email=email, password=password)
    response = requests.post(path + '/rpc/login', data=data).json()
    token = response[0]['token']
    pprint(token)
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(path + '/', headers=headers).json()
    pprint(response)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Test PostgREST Auth')
    argument_parser.add_argument('-e',  help='email', dest='email')
    argument_parser.add_argument('-p',  help='Password', dest='password')
    args = argument_parser.parse_args()
    main(args.email, args.password)
