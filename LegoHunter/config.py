import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ROOT_EMAIL = os.environ.get('ROOT_EMAIL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod 
    def init_app(app): 
        pass 

class DevelopmentConfig(Config): 
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('DEBUG_DATABASE_NAME')}"

class TestingConfig(Config): 
    TESTING = True 
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('TESTING_DATABASE_NAME')}"

class ProductionConfig(Config): 
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('DATABASE_NAME')}"

config = { 
    'development': DevelopmentConfig, 
    'testing': TestingConfig, 
    'production': ProductionConfig, 
    'default': DevelopmentConfig 
}