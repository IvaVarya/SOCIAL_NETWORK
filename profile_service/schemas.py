#schemas.py
from marshmallow import Schema, fields, validate

class ProfileSchema(Schema):
    first_name = fields.Str(required=False, validate=validate.Length(min=1, max=50))  
    last_name = fields.Str(required=False, validate=validate.Length(min=1, max=50))   
    gender = fields.Str(required=False, validate=validate.Length(max=10))           
    date_of_birth = fields.Date(required=False)                                    
    country = fields.Str(required=False, validate=validate.Length(max=50))            
    city = fields.Str(required=False, validate=validate.Length(max=50))              
    profile_picture = fields.Str(required=False)                                      