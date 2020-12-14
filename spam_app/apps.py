from django.apps import AppConfig
import joblib
import os
import logging


class SpamAppConfig(AppConfig):
    name = 'spam_app'
    logging.info(f"Current Path: {os.getcwd}")
    model_path = os.path.abspath(os.path.join('spam_app', 'spam-model', 'pipe_model.pkl'))
    model = joblib.load(model_path)
