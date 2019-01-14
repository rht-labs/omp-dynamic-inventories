#!/usr/bin/env python

import argparse
import requests
import yaml
import os


try:
    import json
except ImportError:
    import simplejson as json


# Define the following environment variables:
# API_URL - The base url for the omp-data-api
# EMAIL_CONTENT_URL - Should be a url which points a yaml file with the email content to send
#                     The yaml file should cointain vars 'body' and 'title'.
# TAG - The tag you want to pull users and groups from.
# USERNAME - The email username from which you want to send notifications from 
# PASSWORD - The password for said username
api_url = os.environ['API_URL']
email_content_url = os.environ['EMAIL_CONTENT_URL']
my_tag = os.environ['TAG']
username = os.environ['EMAIL_USERNAME']
password = os.environ['EMAIL_PASSWORD']


users_url = api_url + "/users"


class Inventory(object):

    def __init__(self):

        self.parse_cli_args()

        self.inventory = {}

        if self.args.list:
            self.handle_list()
        elif self.args.host != None:
            self.handle_host()

        print(json.dumps(self.inventory))


    def handle_list(self):

        my_tag_users = users_url + '/' + my_tag
        r_users = requests.get(my_tag_users).json()
        email_content = yaml.load(requests.get(email_content_url).text)

        mail = {
            "title": email_content['title'],
            "body": email_content['body'],
            "users": self.generate_user_info_list(r_users),
            "email_to": self.generate_send_list(r_users),
            "mail": {
                "host": "smtp.gmail.com",
                "port":"465",
                "secure": "always",
                "username": username,
                "password": password,
                "subtype": "html",
            }
        }

        self.inventory = {'all': { "vars": mail}}

    def generate_send_list(self, user_data):
        send_list = []
        for user in user_data:
            send_list.append(user['email'])

        return send_list

    def generate_user_info_list(self, user_data):
        user_info_list = []
        for user in user_data:
            user_info_list.append({
                'first_name': user['first_name'],
                'username': user['email'].split('@')[0],
                'password': 'foo',
                'email': user['email'],
                'notify_user': True
                })
        return user_info_list


    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory from a file')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


Inventory()
