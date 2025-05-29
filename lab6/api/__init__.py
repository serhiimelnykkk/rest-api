from flask import Flask
from flask_restful import Api
from marshmallow import fields
from .config import Config
from .extensions import db, swagger 
from .schemas import BookSchema 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    swagger.init_app(app)

    api_instance = Api(app) 

    from .resources import initialize_routes

    initialize_routes(api_instance)

    if 'components' not in app.config['SWAGGER']:
        app.config['SWAGGER']['components'] = {}
    if 'schemas' not in app.config['SWAGGER']['components']:
        app.config['SWAGGER']['components']['schemas'] = {}

    def marshmallow_schema_to_openapi_dict(schema_instance):
        openapi_schema = {"type": "object", "properties": {}}
        openapi_schema_required_fields = []

        for field_name, field_obj in schema_instance.fields.items():
            field_type = "string" 
            field_format = None

            if isinstance(field_obj, fields.Int):
                field_type = "integer"
            elif isinstance(field_obj, fields.Bool):
                field_type = "boolean"
            elif isinstance(field_obj, fields.DateTime):
                field_type = "string"
                field_format = "date-time"
            elif isinstance(field_obj, fields.Date):
                field_type = "string"
                field_format = "date"
            elif isinstance(field_obj, fields.Float):
                field_type = "number"
                field_format = "float"

            property_definition = {"type": field_type}
            if field_format:
                property_definition["format"] = field_format
            
            if field_obj.metadata.get('example'):
                property_definition['example'] = field_obj.metadata.get('example')
            if field_obj.metadata.get('description'):
                property_definition['description'] = field_obj.metadata.get('description')

            openapi_schema["properties"][field_name] = property_definition
            
            if field_obj.required:
                openapi_schema_required_fields.append(field_name)
            if field_obj.dump_only:
                 openapi_schema["properties"][field_name]["readOnly"] = True
            if field_obj.load_only:
                openapi_schema["properties"][field_name]["writeOnly"] = True
        
        if openapi_schema_required_fields:
            openapi_schema["required"] = openapi_schema_required_fields
            
        return openapi_schema

    app.config['SWAGGER']['components']['schemas']['Book'] = marshmallow_schema_to_openapi_dict(BookSchema())
    app.config['SWAGGER']['components']['schemas']['BookInput'] = marshmallow_schema_to_openapi_dict(BookSchema(exclude=('id',)))

    if not hasattr(create_app, 'routes_printed'): 
        with app.app_context(): 
            print("=" * 50)
            print("REGISTERED ROUTES IN create_app() (final check):")
            for rule in app.url_map.iter_rules():
                print(f"Rule: {rule}, Methods: {','.join(sorted(list(rule.methods)))}, Endpoint: {rule.endpoint}")
            print("=" * 50)
            create_app.routes_printed = True


    return app