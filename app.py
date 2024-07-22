from  flask import Flask
from flasgger import Swagger
from api.routes.insurance_api import insurance_api
from api.routes.customer_api import customer_api
from api.routes.policy_api import policy_api

def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title' : 'Insurance API kits'
    }

    swagger = Swagger(app=app)
    app.config.from_pyfile('config.py')
    app.register_blueprint(insurance_api, url_prefix='/api/v1/llm')
    app.register_blueprint(customer_api, url_prefix='/api/v1/sql')
    app.register_blueprint(policy_api, url_prefix='/api/v1/sql')

    return app

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # parser.add_argument('-p', '--port', default=8000, type=int, help='port to listen on')
    parser.add_argument('-p', '--port', type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    app.run(port=port, debug=True)