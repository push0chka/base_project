from src.app.application import create_app
from src.app.settings.environment import Environment

app = create_app(Environment.TEST)
