import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://user_lab6:password_lab6@localhost:5436/librarydb_lab6' 
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10 

    SWAGGER = {
        'title': 'Library API (Flask-RESTful)',
        'uiversion': 3, 
        'openapi': '3.0.2',
        'specs_route': '/apidocs/', 
        'doc_expansion': 'list', 
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/apispec_1.json',
                'rule_filter': lambda rule: True,  
                'model_filter': lambda tag: True, 
            }
        ],
        "components": {
            "securitySchemes": {

            }
        },
    }