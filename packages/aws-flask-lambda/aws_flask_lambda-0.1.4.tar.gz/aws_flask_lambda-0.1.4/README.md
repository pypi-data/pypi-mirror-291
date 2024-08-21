# aws_flask_lambda

Version 0.1.3 updates Flask and werkzeug version requirements to 3.0.3 and updates werkzeug.wrappers import, from base_request.py to request.py

Version 0.1.4 fixes an error when extracting the event['body'] on the AWS environment request, on the environ variable 'wsgi.input'

## Installation

Install the package using pip:

```sh
pip install aws-flask-lambda
```

## Usage

```python
from aws_flask_lambda import FlaskLambda
from flask import request, jsonify

app = FlaskLambda(__name__)


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    name = request.form.get('name', 'World')
    message = f'Hello, {name}!'
    return (
        jsonify({'message': message}),
        200,
        {'Content-Type': 'application/json'}
    )


if __name__ == '__main__':
    app.run(debug=True)

```
