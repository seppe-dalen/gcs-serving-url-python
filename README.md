### Resize your image files on Google Cloud storage with [Images Python API](https://developers.google.com/appengine/docs/python/images/) powered by Google.

## Setup

1. Clone this repo.

```
git clone https://github.com/seppe-dalen/gcs-serving-url-python
```

2. Install the requirements.

```
pip install -r requirements.txt -t lib
```

3. Deploy to App Engine.

```
gcloud app deploy
```
Ensure the targetted bucket and the app engine instance are in the same region

4. Grant app engine service account permission to the bucket.
* Find your app engine service account in the `IAM & Admin` section, copy it
* Search for `cloud storage` in GCP
* Click into a bucket (create a bucket if you don't have any)
* Go to the permissions tab and add the service account to the permissions with the role `Storage Legacy Bucket Owner` 


## Usage

1. Get a serving url from existed file on Google Cloud Storage:

```
curl https://PROJECT_NAME.appspot.com/image-url?bucket=mybuckey&image=image_name.jpg
```

2. It will return a url that looks something like:

```
https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg
```

## Reminders

1. Only one app can "own" the image. As stated in the [documentation](https://developers.google.com/appengine/docs/python/images/functions) for get_serving_url:

> If you serve images from Google Cloud Storage, you cannot serve an image from two separate apps. Only the first app that calls get_serving_url on the image can get the URL to serve it because that app has obtained ownership of the image.

2. The serving url is inherently public (no support for private serving urls) but made in a non guessable way.

## Advanced Parameters

### SIZE / CROP

* **s640** — generates image 640 pixels on largest dimension
* **s0** — original size image
* **w100** — generates image 100 pixels wide
* **h100** — generates image 100 pixels tall
* **s** (without a value) — stretches image to fit dimensions
* **c** — crops image to provided dimensions
* **n** — same as c, but crops from the center
* **p** — smart square crop, attempts cropping to faces
* **pp** — alternate smart square crop, does not cut off faces (?)
* **cc** — generates a circularly cropped image
* **ci** — square crop to smallest of: width, height, or specified =s parameter
* **nu** — no-upscaling. Disables resizing an image to larger than its original resolution.