import psycopg2
import etcd
from flask import Flask, g
from flask_restful import Api
from api.account import RegistrationResource, VerificationResource, AccessTokenResource

app = Flask(__name__)
api = Api(app)

api.add_resource(RegistrationResource, '/registration')
api.add_resource(VerificationResource, '/verification')
api.add_resource(AccessTokenResource, '/access')


@app.before_first_request
def load_config():
    client = etcd.Client(host='172.17.0.1', port=2379)
    g.token_secret = client.read('/token/secret').value
    g.database_config = client.read('/database/app', recursive=True, sorted=True)
    g.smtp_config = client.read('/email/smtp', recursive=True, sorted=True)


@app.before_request
def before_request():
    g.db = psycopg2.connect(g.database_config)


@app.teardown_request
def teardown_request(e):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
