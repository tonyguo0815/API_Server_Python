from flask import Flask;

from router.example import example_blueprints;

app = Flask(__name__);

@app.route('/')
def index():
    return 'This is API Server'

app.register_blueprint(example_blueprints, url_prefix='/example');

if __name__ == "__main__":
    app.run(debug=True)