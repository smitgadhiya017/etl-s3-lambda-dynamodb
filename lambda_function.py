import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("clean_records")

def get_risk_level(magnitude):
    if magnitude >= 5:
        return "High"
    elif magnitude >= 3:
        return "Medium"
    return "Low"

def lambda_handler(event, context):

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)

    data = json.loads(response["Body"].read())

    total_records = 0
    inserted_records = 0
    rejected_records = 0

    for feature in data.get("features", []):

        total_records += 1

        earthquake_id = feature.get("id")
        props = feature.get("properties", {})

        magnitude = props.get("mag")
        place = props.get("place")
        timestamp = props.get("time")

        if earthquake_id is None or magnitude is None:
            rejected_records += 1
            continue

        item = {
            "record_id": earthquake_id,
            "place": place.title() if place else "Unknown",
            "magnitude": round(float(magnitude), 1),
            "timestamp": datetime.utcfromtimestamp(timestamp / 1000).isoformat(),
            "risk_level": get_risk_level(float(magnitude))
        }

        table.put_item(Item=item)
        inserted_records += 1

    print({
        "total_records": total_records,
        "inserted_records": inserted_records,
        "rejected_records": rejected_records,
        "processed_at": datetime.utcnow().isoformat()
    })

    return {
        "statusCode": 200,
        "body": json.dumps("ETL Completed Successfully")
    }