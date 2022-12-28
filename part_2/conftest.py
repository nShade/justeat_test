import logging
import pytest
import yaml


@pytest.fixture(scope='session')
def configuration():
    with open('part_2/configuration.yaml', 'r') as file:
        config = yaml.safe_load(file)

    return config


@pytest.fixture(scope='function')
def debug(caplog):
    caplog.set_level(logging.DEBUG)