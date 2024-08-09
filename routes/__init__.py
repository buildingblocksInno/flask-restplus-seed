from flask import Flask
from flask_restx import Api, Namespace, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)
api = Api(app)

auth_ns = Namespace('auth', description='Authentication operations')

user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

users = []  # This will act as a mock database for demonstration

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(user_model)
    @auth_ns.doc('user_signup')
    def post(self):
        data = auth_ns.payload
        if any(user['username'] == data['username'] for user in users):
            return {'message': 'User already exists'}, 409
        users.append(data)
        return {'message': 'User created successfully'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_model)
    @auth_ns.doc('user_login')
    def post(self):
        data = auth_ns.payload
        user = next((user for user in users if user['username'] == data['username'] and user['password'] == data['password']), None)
        if not user:
            return {'message': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=user['username'])
        return {'access_token': access_token}, 200

@auth_ns.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, {current_user}'}, 200

api.add_namespace(auth_ns, path='/auth')

if __name__ == '__main__':
    app.run(debug=True)
