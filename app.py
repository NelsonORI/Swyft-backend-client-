from flask import Flask
from flask_migrate import Migrate
import config  # Import your configuration
from extensions import swyft_db  # Import the db instance from extensions.py

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize Flask-Migrate with the app and the swyft_db instance
migrate = Migrate(app, swyft_db)

# Initialize the swyft_db instance with the app
swyft_db.init_app(app)

# Import and register the Blueprint after app initialization
from routes import api  # Import the Blueprint from routes.py
app.register_blueprint(api, url_prefix='/api')  # Register the blueprint

# To avoid circular imports, place any additional app-related imports here
if __name__ == '__main__':
    app.run(debug=True)
