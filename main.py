from flask import Flask
from flask_cors import CORS
from config import Config
from v1.database import db
from v1.schemas import ma
from v1.api import api, jwt
from dotenv import load_dotenv

load_dotenv()


def main():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    ma.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app.run(debug=True)


if __name__ == '__main__':
    main()
