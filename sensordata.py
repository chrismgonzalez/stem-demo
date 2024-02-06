#!/usr/bin/env python3

#
# sensordata.py
#


# Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

#
# import useful stuff
#

import datetime
import json
import logging
import random
import threading
import time

import boto3

#
# globals
#

session = boto3.Session(profile_name='cmgs-prod', region_name='us-east-2')
TOPIC_BASE = 'dt/sensor'
REGION = 'us-east-2'
DATA_ENDPOINT = session.client('iot', region_name=REGION).describe_endpoint(
    endpointType='iot:Data-ATS'
)['endpointAddress']
C_IOT_DATA = session.client(
    'iot-data',
    region_name=REGION,
    endpoint_url=f'https://{DATA_ENDPOINT}'
)

SENSORS = {
    'sensor_01': {'building': 'BGE', 'room': 'Hanks'},
    'sensor_02': {'building': 'BGE', 'room': 'Whitacre'},
    'sensor_03': {'building': 'BGE', 'room': 'Smith'},
    'sensor_04': {'building': 'BGE', 'room': 'Williams'},
    'sensor_05': {'building': 'BGE', 'room': 'Parker'},
    'sensor_06': {'building': 'SMG', 'room': 'Gonzalez'},
    'sensor_07': {'building': 'SMG', 'room': 'Deal'},
    'sensor_08': {'building': 'SMG', 'room': 'Curry'},
}

#
# Configure logging
#
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s - %(levelname)s - \
%(filename)s:%(lineno)s - %(funcName)s - %(message)s")
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def sensor_data():
    message = {}
    message['temperature'] = random.uniform(33, 35)
    message['humidity'] = random.uniform(68, 70)
    message['pressure'] = random.uniform(1145, 1150)

    return message

def send_sensor_data(thing):
    while True:
        try:
            message = sensor_data()

            message['device_id'] = thing
            message['building'] = SENSORS[thing]['building']
            message['room'] = SENSORS[thing]['room']

            topic = '{}/{}'.format(TOPIC_BASE, thing)
            logger.info("publish: topic: %s message: %s", topic, message)

            response = C_IOT_DATA.publish(topic=topic, qos=0, payload=json.dumps(message))
            logger.info("response: %s", response)
        except Exception as error:
            logger.error("%s", error)

        time.sleep(2)


for sensor in SENSORS.keys():
    logger.info("starting thread for sensor: %s", sensor)
    threading.Thread(target=send_sensor_data, args=(sensor,)).start()


start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
while True:
    logger.info("%s: start_time: %s now: %s threads:",
                __file__, start_time,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for thread in threading.enumerate():
        logger.info("  %s", thread)

    time.sleep(30)
