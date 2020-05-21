#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Thursday, May 21st 2020, 4:52:58 pm
# Author: Charlene Leong charleneleong84@gmail.com
# Last Modified: Thursday, May 21st 2020, 7:08:09 pm
###


import boto3
import os

from os import system, name 
from os.path import expanduser
from pathlib import Path
import json
from datetime import datetime
import time
import configparser
import argparse

CONFIG_FILEPATH = os.path.join(os.getcwd(), 'sso_config')


def get_cache():
    home = expanduser('~')
    cache = os.path.join(home,'.aws','sso','cache')
    test = os.path.isdir(cache)
    if test:
        return cache
    else:
        print('An ~/.aws/sso folder was not found. Please ensure you have configured and logged into AWS SSO before using.')
        exit()


def get_sso_credentials(cache):
    file_list = os.listdir(cache)
    for file in file_list:
        if file[0:18] != 'botocore-client-id':
            cached_credentials_fname = file
            found_flag = True
    file = os.path.join(cache, cached_credentials_fname)
    with open(file, 'r') as f:
        data = f.read()
    return json.loads(data)


def get_aws_account_list(region, access_token):
    client = boto3.client('sso', region_name=region)
    accounts = client.list_accounts(
        maxResults=999,
        accessToken=access_token
    )
    return accounts['accountList']



def check_expired_credentials(sso_credentials):
    expiration = sso_credentials['expiresAt']
    expiration_s = datetime.strptime(expiration, '%Y-%m-%dT%H:%M:%SUTC')
    current_datetime = datetime.utcnow()
    if current_datetime >= expiration_s:
        print(f'SSO Access Token has expired. Please login again with the following command - aws sso login --profile primary')
        exit()
    return False



def load_sso_profile():
    print(f'Loading SSO profile from ~/.aws/config')
    home = expanduser('~')
    config = configparser.ConfigParser()
    config_path = config.read(f'{home}/.aws/config')
    return dict(config['profile primary'])



def create_new_sso_profile(sso_profile, accounts, region, access_token):
    client = boto3.client('sso', region_name=region)
    config = configparser.ConfigParser()
    config['profile_primary'] = sso_profile
    
    for account in accounts:
        roles = client.list_account_roles(
            maxResults = 999,
            accessToken = access_token,
            accountId = account['accountId']
        )
        account_name = account['accountName']
        account_name = account['accountName'].replace(' ','')
        for role in roles['roleList']:
            role_name = role['roleName']
            account_id = role['accountId']
            section_name = 'profile ' + account_name + '-' + role_name
            config.add_section(section_name)
            config.set(section_name, 'sso_start_url', sso_profile['sso_start_url'])
            config.set(section_name, 'sso_region', sso_profile['sso_region'])
            config.set(section_name, 'sso_account_id', account_id)
            config.set(section_name, 'sso_role_name', role_name)
            config.set(section_name, 'region', sso_profile['region'])
            config.set(section_name, 'output', sso_profile['output'])
        
    with open(CONFIG_FILEPATH, 'w') as configfile:
        config.write(configfile)
    


def main():
    cache = get_cache()
    sso_credentials = get_sso_credentials(cache)
    if not check_expired_credentials(sso_credentials):    
        access_token = sso_credentials['accessToken']
        region = sso_credentials['region']
        sso_profile = load_sso_profile()
        accounts = get_aws_account_list(region, access_token)
        create_new_sso_profile(sso_profile,accounts, region, access_token)
        


if __name__ == '__main__':
    main()