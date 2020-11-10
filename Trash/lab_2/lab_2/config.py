import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    current_path = os.getcwd()

    WORKING_FOLDER = current_path + '/app/'
