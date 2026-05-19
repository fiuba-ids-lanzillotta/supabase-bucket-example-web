import logging
from flask import Flask
from bucket_example_web.routes.mascotas import mascotas_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.json.sort_keys = False

app.register_blueprint(mascotas_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
