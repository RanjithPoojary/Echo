import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' +os.path.join(basedir, 'app.db')

    # Mail configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # Configurations to use if gmail in-use.
    # MAIL_SERVER = "smtp.googlemail.com"
    # MAIL_PORT = 587
    # MAIL_USE_TLS = 1
    # MAIL_USERNAME = "<your-gmail-username>"
    # MAIL_PASSWORD = "<your-gmail-password>"