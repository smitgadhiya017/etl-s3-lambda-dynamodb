import csv
import json
import boto3
import traceback
from io import StringIO
from decimal import Decimal
from datetime import datetime

# AWS Clients
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

        csv_content = response["Body"].read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(csv_content))

        for row in csv_reader:

            total_records += 1

            earthquake_id = row.get("record_id")
            place = row.get("place")
            magnitude = row.get("magnitude")
            event_time = row.get("event_time")

            if not earthquake_id or not magnitude:
                rejected_records += 1
                continue

            try:
                magnitude = Decimal(str(magnitude))
            except:
                rejected_records += 1
                continue

            item = {
                "record_id": str(earthquake_id),
                "place": place if place else "Unknown",
                "magnitude": magnitude,
                "risk_level": get_risk_level(float(magnitude)),
                "file_type": "csv",
                "event_time": event_time,
                "processed_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }

            table.put_item(Item=item)

            inserted_records += 1

        print("========== CSV ETL SUMMARY ==========")
        print(f"Total Records    : {total_records}")
        print(f"Inserted Records : {inserted_records}")
        print(f"Rejected Records : {rejected_records}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "CSV ETL Completed Successfully",
                "total": total_records,
                "inserted": inserted_records,
                "rejected": rejected_records
            })
        }

    except Exception as e:

        print("========== ERROR ==========")
        print(str(e))
        traceback.print_exc()

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }