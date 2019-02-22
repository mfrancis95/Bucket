from flask import Flask, render_template, request
from boto3 import client
from os import environ

app = Flask(__name__)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
app.url_map.strict_slashes = False

_s3 = client(
    's3', aws_access_key_id = environ['S3_KEY'],
    aws_secret_access_key = environ['S3_SECRET'],
    endpoint_url = environ['S3_ENDPOINT']
)

@app.route('/copy', methods = ['POST'])
def copy():
    errors = []
    for key in request.json:
        try:
            _s3.copy_object(
                Bucket = environ['S3_BUCKET'],
                CopySource = f'{environ["S3_BUCKET"]}/{key}',
                Key = 'Copy of ' + key
            )
        except:
            errors.append(key)
    if errors:
        if len(errors) == len(request.json):
            return '', 500
        return 'Some objects were not able to be copied.', 205
    return '', 205

@app.route('/delete', methods = ['POST'])
def delete():
    for key in request.json:
        _s3.delete_object(Bucket = environ['S3_BUCKET'], Key = key)
    return '', 205

@app.route('/')
def index():
    return render_template(
        'index.html',
        objects = _s3.list_objects(Bucket = environ['S3_BUCKET'])['Contents']
    )