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

from datetime import datetime, timedelta
import logging

import click

from pywis_pubsub import cli_options
from pywis_pubsub.util import yaml_load
from pywis_pubsub.storage import STORAGES

from wis2_gc.env import PYWIS_PUBSUB_CONFIG, STORAGE_DATA_RETENTION_DAYS

LOGGER = logging.getLogger(__name__)


class Cacher:
    def __init__(self):
        with open(PYWIS_PUBSUB_CONFIG) as fh:
            pywis_pubsub_config = yaml_load(fh)

        storage_class = STORAGES[pywis_pubsub_config.get('storage').get('type')]  # noqa
        self.storage_object = storage_class(pywis_pubsub_config['storage'])

    def setup(self) -> None:
        """Setup storage backend"""
        _ = self.storage_object.setup()

    def teardown(self) -> bool:
        """Setup storage backend"""
        _ = self.storage_object.teardown()

    def clean(self, days: int = 2) -> None:
        """Clean storage"""

        today = datetime.utcnow().date()

        for obj, last_modified in self.storage_object.list_contents_by_date():
            delta = today - timedelta(days=days)
            last_modified = last_modified.date()
            if last_modified < delta:
                LOGGER.info(f'Deleting {obj}')
                self.storage_object.delete(obj)

        return


@click.command()
@click.pass_context
@click.option('--days', '-d', help='Number of days of data to keep', type=int)
@cli_options.OPTION_VERBOSITY
def clean(ctx, days, verbosity):
    """Clean data directories and API indexes"""

    if days is not None:
        days_ = days
    else:
        days_ = STORAGE_DATA_RETENTION_DAYS

    if days_ is None or days_ < 0:
        click.echo('No data retention set. Skipping')
    else:
        click.echo(f'Cleaning data older than {days} days')
        c = Cacher()
        c.clean(days)


@click.command()
@click.pass_context
@click.option('--yes', '-y', 'bypass', is_flag=True, default=False,
              help='Bypass permission prompts')
@cli_options.OPTION_VERBOSITY
def setup(ctx, bypass, verbosity='NOTSET'):
    """Create GC backend"""

    if not bypass:
        if not click.confirm('Create GC backend?  This will overwrite existing storage', abort=True):  # noqa
            return

    c = Cacher()
    c.setup()


@click.command()
@click.pass_context
@click.option('--yes', '-y', 'bypass', is_flag=True, default=False,
              help='Bypass permission prompts')
@cli_options.OPTION_VERBOSITY
def teardown(ctx, bypass, verbosity='NOTSET'):
    """Delete GC backend"""

    if not bypass:
        if not click.confirm('Delete GC backend?  This will remove existing storage', abort=True):  # noqa
            return

    c = Cacher()
    c.teardown()
