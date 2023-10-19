###############################################################################
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

from datetime import datetime
import json
import logging

from pywis_pubsub.hook import Hook
from pywis_pubsub.message import get_link
from pywis_pubsub.mqtt import MQTTPubSubClient

from wis2_gc.env import BROKER_URL, URL

LOGGER = logging.getLogger(__name__)


class DataMetadataHook(Hook):
    def execute(self, topic: str, msg_dict: dict) -> None:
        LOGGER.debug('Data and metadata hook execution begin')

        m = self.client or MQTTPubSubClient(BROKER_URL)

        LOGGER.debug('Adjusting link from origin to cache')
        cache_link = origin_link = get_link(msg_dict['links'])
        LOGGER.debug('Adjusting topic from origin to cache')
        cache_topic = topic.replace('origin/', 'cache/', 1)

        cache_link['href'] = f"{URL}/{msg_dict['properties']['data_id']}"

        for link2 in msg_dict['links']:
            if link2['rel'] == origin_link['rel']:
                msg_dict['links'].remove(origin_link)

        msg_dict['links'].append(cache_link)

        LOGGER.debug('Updating pubtime')
        datetime_ = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        msg_dict['properties']['pubtime'] = datetime_

        LOGGER.debug(f'Publishing message to {cache_topic}')
        m.pub(cache_topic, json.dumps(msg_dict))

        LOGGER.debug('Data and metadata hook execution end')
