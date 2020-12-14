from django.apps import AppConfig
import joblib
import os


class SpamAppConfig(AppConfig):
    name = 'spam_app'
    model_path = os.path.abspath(os.path.join('spam-model', 'pipe_model.pkl'))
    model = joblib.load(model_path)
