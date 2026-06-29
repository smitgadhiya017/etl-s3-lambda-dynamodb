import json
import boto3
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "clean_records"
table = dynamodb.Table(TABLE_NAME)


def get_risk_level(magnitude):
    if magnitude >= 5:
        return "High"
    elif magnitude >= 3:
        return "Medium"
    else:
        return "Low"


def lambda_handler(event, context):

    total_records = 0
    inserted_records = 0
    rejected_records = 0

    try:

        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]

        print(f"Bucket : {bucket}")
        print(f"File   : {key}")

        response = s3.get_object(Bucket=bucket, Key=key)

        data = json.loads(response["Body"].read().decode("utf-8"))

        for feature in data.get("features", []):

            total_records += 1

            earthquake_id = feature.get("id")
            props = feature.get("properties", {})

            magnitude = props.get("mag")
            place = props.get("place")
            timestamp = props.get("time")

            # Skip invalid records
            if earthquake_id is None or magnitude is None:
                rejected_records += 1
                continue

            item = {
                "record_id": earthquake_id,
                "place": place if place else "Unknown",
                "magnitude": round(float(magnitude), 1),
                "risk_level": get_risk_level(float(magnitude)),
                "event_time": datetime.utcfromtimestamp(
                    timestamp / 1000
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "processed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }

            table.put_item(Item=item)

            inserted_records += 1

        print("===== ETL SUMMARY =====")
        print(f"Total Records    : {total_records}")
        print(f"Inserted Records : {inserted_records}")
        print(f"Rejected Records : {rejected_records}")

        return {
            "statusCode": 200,
            "body": json.dumps("ETL Completed Successfully")
        }

    except Exception as e:

        print("ERROR :", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }