import os,sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)
sys.path.insert(0, path)

import pytest
from sportsbetx import create_app

# with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
#     _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': 'postgresql',
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()