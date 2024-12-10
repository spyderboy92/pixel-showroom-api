from flask_restx import Namespace, Resource

# Define the default namespace
api = Namespace('TestServer', description='Test if server is online', path='/')


@api.route('/test')
class HelloWorld(Resource):

    @api.doc(description='Returns a hello world message')
    def get(self):
        return {'message': 'Hello World, I am online!'}
