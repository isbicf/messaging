from flask import Flask
from messaging.config import Config
from messaging.api.message import message_bp

print(">>> USING SQLITE:", Config.DB_PATH)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register API routes
    app.register_blueprint(message_bp, url_prefix='/messages')

    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200

    return app


# Optional local runner (Docker uses: python -m messaging.app)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
