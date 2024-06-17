###############################################################################
#
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

import os

URL = os.environ.get('WIS2_GC_URL')
STORAGE_DATA_RETENTION_DAYS = os.environ.get(
    'WIS2_GC_STORAGE_DATA_RETENTION_DAYS')

STORAGE_URL = os.environ.get('WIS2_GC_STORAGE_URL')
STORAGE_PATH = os.environ.get('WIS2_GC_STORAGE_PATH')

PYWIS_PUBSUB_CONFIG = os.environ.get('WIS2_GC_PYWIS_PUBSUB_CONFIG')
BROKER_URL = os.environ.get('WIS2_GC_BROKER_URL')
