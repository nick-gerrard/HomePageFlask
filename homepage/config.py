import json

def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

config_dict = get_json_data('/configs/HomePageConfigs.json')


class Config:
    SECRET_KEY = config_dict['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config_dict['SQLALCHEMY_DATABASE_URI']
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = config_dict['MAIL_USERNAME']
    MAIL_PASSWORD = config_dict['MAIL_PASSWORD']