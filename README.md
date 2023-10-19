[![flake8](https://github.com/wmo-im/wis2-gc/workflows/flake8/badge.svg)](https://github.com/wmo-im/wis2-gc/actions)

# wis2-gc

wis2-gc is a Reference Implementation of a WIS2 Global Cache.

<em>Note: architecture diagrams referenced from the <a href="https://github.com/wmo-im/wis2-guide">WIS2 Guide</a></em>

<a href="https://github.com/wmo-im/wis2-guide/blob/main/guide/images/architecture/c4.component-gc.png"><img alt="WIS2 GC C4 component diagram" src="https://github.com/wmo-im/wis2-guide/raw/main/guide/images/architecture/c4.component-gc.png" width="800"/></a>

## Workflow

- connects to a WIS2 Global Broker, subscribed to the following:
  - `origin/a/wis2/#1
- on all notifications:
  - download and store data to object storage
  - publish notification of cached object

## Installation

### Requirements
- Python 3
- [virtualenv](https://virtualenv.pypa.io)

### Dependencies
Dependencies are listed in [requirements.txt](requirements.txt). Dependencies
are automatically installed during pywis-pubsub installation.

### Installing wis2-gc

```bash
# setup virtualenv
python3 -m venv --system-site-packages wis2-gc
cd wis2-gc
source bin/activate

# clone codebase and install
git clone https://github.com/wmo-im/wis2-gc.git
cd wis2-gc
pip3 install .
```

## Running

```bash
# setup environment and configuration
cp wis2-gc.env local.env
vim local.env # update accordingly

source local.env

# setup pywis-pubsub - sync WIS2 notification schema
pywis-pubsub schema sync

# setup backend
wis2-gc setup

# teardown backend
wis2-gc teardown

# connect to Global Broker
# notifications will automatically trigger wis2-gc to cache data
# and send a notification to the local broker
pywis-pubsub subscribe --config pywis-pubsub.yml --download

# cleanup data older than n days (default is 2)
wis2-gc clean --days 3
```

### Docker

Instructions to run wis2-gc via Docker can be found the [`docker`](docker) directory.

## Development

### Running Tests

```bash
# install dev requirements
pip3 install -r requirements-dev.txt

# run tests like this:
python3 tests/run_tests.py

# or this:
python3 setup.py test
```

### Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

### Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/wmo-im/wis2-gc/issues).

## Contact

* [Tom Kralidis](https://github.com/tomkralidis)
