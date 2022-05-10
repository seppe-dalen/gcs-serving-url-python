#!/usr/bin/python

import json

from flask import Flask, request, make_response

from google.appengine.ext import blobstore
from google.appengine.api import images, wrap_wsgi_app

JSON_MIME_TYPE = 'application/json'

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)

@app.route('/image-url', methods=['GET'])
def image_url():
	bucket = request.args.get('bucket')
	image = request.args.get('image')

	if not all([bucket, image]):
		error = json.dumps({'error': 'Missing `bucket` or `image` parameter.'})
		return json_response(error, 422)

	filename = ('/gs/' + bucket + "/" + image)

	try:
		blobKey = blobstore.create_gs_key(filename)
	except blobstore.BlobNotFoundError:
		error = json.dumps({'error': 'Blob not found'})
		return json_response(error, 401)
	except blobstore.PermissionDeniedError:
		error = json.dumps({'error': 'Permission denied'})
		return json_response(error, 400)

	try:
		servingImage = images.get_serving_url(blobKey)
	except images.AccessDeniedError:
		error = json.dumps({'error': 'Permission denied'})
		return json_response(error, 401)
	except images.ObjectNotFoundError:
		error = json.dumps({'error': 'The file was not found.'})
		return json_response(error, 404)
	except images.TransformationError:
		error = json.dumps({'error': 'There was a problem transforming the image.'})
		return json_response(error, 400)

	return json_response(json.dumps({'url': servingImage}))

def json_response(data='', status=200, headers=None):
	headers = headers or {}
	if 'Content-Type' not in headers:
		headers['Content-Type'] = JSON_MIME_TYPE

	return make_response(data, status, headers)
