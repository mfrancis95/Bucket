from flask import Flask, render_template
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

@app.route('/')
def index():
    return render_template(
        'index.html',
        objects = _s3.list_objects(Bucket = environ['S3_BUCKET'])['Contents']
    )