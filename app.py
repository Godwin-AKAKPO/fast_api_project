from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, title='API')

ns = api.namespace('hello', description='Hello operations')

@ns.route('/')
class HelloResource(Resource):
    def get(self):
        """Retourne un message de bienvenue"""
        return {'message': 'Bonjour depuis votre API Flask '}

if __name__ == '__main__':
    app.run(debug=True)
