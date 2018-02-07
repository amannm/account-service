from flask import Flask
from flask_restful import Api
from api.account import AccountResource

app = Flask(__name__)
api = Api(app)

api.add_resource(AccountResource, '/accounts')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
