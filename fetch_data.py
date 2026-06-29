import json
import boto3
import urllib.request
from datetime import datetime

BUCKET_NAME = "smit-earthquake-etl-2026"

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

response = urllib.request.urlopen(URL)

data = json.loads(response.read().decode())

filename = f"raw/earthquake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

s3 = boto3.client("s3")

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=filename,
    Body=json.dumps(data),
    ContentType="application/json"
)

print("Uploaded:", filename)