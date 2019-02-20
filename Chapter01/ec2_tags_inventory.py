#!/usr/bin/env python

import boto3
import json
import ConfigParser
import os

def get_name(instance):
    name = "Null"
    if 'Tags' in instance.keys():
        for tag in instance['Tags']:
            if 'Key' in tag and tag['Key'] == "Name":
                name = str(tag['Value'])
    return name 

if os.path.isfile('ec2.ini'):
	config_path = 'ec2.ini'
elif os.path.isfile(os.path.expanduser('~/ec2.ini')):
	config_path = os.path.expanduser('~/ec2.ini')

config = ConfigParser.ConfigParser()
config.read(config_path)
id = config.get("credentials", "aws_access_key_id", raw=True)
key = config.get("credentials", "aws_secret_access_key", raw=True)

client = boto3.client('ec2', aws_access_key_id = id, aws_secret_access_key = key, region_name = "us-west-2")

inventory = {}

reservations = client.describe_instances()['Reservations']
for reservation in reservations:
    for instance in reservation['Instances']:
        name = get_name(instance)
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if 'Key' in tag and tag['Key'] == "zc-env":
                    roles = tag['Value'].split(",")
                    for role in roles:
                        if role in inventory:
                            inventory[role].append(name)
                        else:
                            inventory[role] = [name]

#print json.dumps(inventory)

print "\nmachine categories: ", inventory.keys()

print "\n%d dev machines: " % len(inventory['dev']), inventory['dev']
print "\n%d ops machines: " % len(inventory['ops']), inventory['ops']
print "\n%d demo machines: " % len(inventory['demo']), inventory['demo']
print "\n%d testing machines: " % len(inventory['testing']), inventory['testing']
print "\n%d staging machines: " % len(inventory['staging']), inventory['staging']
print "\n%d production machines: " % len(inventory['production']), inventory['production']
print "\n%d x2 machines: " % len(inventory['x2']), inventory['x2']
