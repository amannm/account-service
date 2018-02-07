from flask import Flask
from flask_restful import Api
from api.account import RegistrationResource, VerificationResource, AccessTokenResource

app = Flask(__name__)
api = Api(app)

api.add_resource(RegistrationResource, '/registration')
api.add_resource(VerificationResource, '/verification')
api.add_resource(AccessTokenResource, '/access')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
