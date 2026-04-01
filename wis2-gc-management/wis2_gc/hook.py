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

import logging

from pywis_pubsub.hook import Hook
from pywis_pubsub.mqtt import MQTTPubSubClient
import redis

from wis2_gc.cacher import Cacher
from wis2_gc.env import CACHE_URL, CACHE_RETENTION_SECONDS
from wis2_gc.env import BROKER_URL

LOGGER = logging.getLogger(__name__)


class DataMetadataHook(Hook):
    def execute(self, topic: str, msg_dict: dict) -> None:

        self.cache = redis.Redis().from_url(CACHE_URL)

        LOGGER.debug('Checking for duplicate message')
        if self.cache.get(msg_dict['id']) is not None:
            msg = f"Duplicate message {msg_dict['id']}; discarding"
            LOGGER.info(msg)
            return
        else:
            msg = f"New message {msg_dict['id']}; adding"
            LOGGER.info(msg)
            self.cache.set(
                msg_dict['id'],
                msg_dict['properties']['data_id'],
                nx=True,
                ex=CACHE_RETENTION_SECONDS
            )

        LOGGER.debug('Data and metadata hook execution begin')
        m = self.client or MQTTPubSubClient(BROKER_URL)
        c = Cacher()
        c.publish(topic, msg_dict, m)
        LOGGER.debug('Data and metadata hook execution end')
