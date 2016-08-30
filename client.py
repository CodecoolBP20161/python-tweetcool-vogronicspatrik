import argparse
import ipaddress
import os
import requests
import time

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host",
                    help="IP address of the Tweetcool server",
                    default='192.168.160.10')  # Equals 'localhost'
parser.add_argument("-P", "--port",
                    help="Post used by the Tweetcool server",
                    type=int,
                    default=9876)
args = parser.parse_args()

try:
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])

# Logic starts here... somewhere..
on = True

while on:
    os.system('clear')
    response = requests.get(server['address'] + '/tweet')
    for tweet in response.json():
        print(tweet['poster'] + ' said: ' + tweet['content'] + ' when: ' + str(time.ctime(tweet['timestamp'])))
    get_input = input('Who are you?')
    if get_input != 'x':
        get_input_sec = input('your message:')
        msg = {'poster': get_input, 'content': get_input_sec}
        requests.post(server['address'] + '/tweet', json=msg)
    else:
        on = False
