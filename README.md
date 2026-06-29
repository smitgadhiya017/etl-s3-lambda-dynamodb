# Earthquake Serverless ETL Pipeline

## Project Overview

This project demonstrates a complete **Serverless ETL (Extract, Transform, Load) Pipeline** on AWS. The pipeline automatically processes earthquake data from the USGS Earthquake API, stores raw data in Amazon S3, transforms the data using AWS Lambda, and loads the cleaned records into Amazon DynamoDB.

The project also implements a complete **CI/CD pipeline** using GitHub, GitHub Actions, AWS CodeBuild, and AWS CodePipeline for automatic deployment.

---

## Architecture

```text
USGS Earthquake API
          │
          ▼
    fetch_data.py
          │
          ▼
      Amazon S3
     (raw folder)
          │
          ▼
      S3 Event Trigger
          │
          ▼
     AWS Lambda ETL
          │
          ▼
 Transform & Validate
          │
          ▼
 Amazon DynamoDB
(clean_records table)
          │
          ▼
 Amazon CloudWatch Logs

GitHub Repository
        │
        ▼
 GitHub Actions
        │
        ▼
 AWS CodeBuild
        │
        ▼
 AWS CodePipeline
        │
        ▼
 AWS Lambda Deployment
```

---

## AWS Services Used

* Amazon S3
* AWS Lambda
* Amazon DynamoDB
* Amazon CloudWatch
* AWS IAM
* AWS CodeBuild
* AWS CodePipeline
* GitHub
* GitHub Actions

---

## Project Workflow

### Step 1 – Extract

The Python script (`fetch_data.py`) downloads the latest earthquake data from the USGS Earthquake API.

```
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson
```

The downloaded JSON file is uploaded automatically to:

```
s3://smit-earthquake-etl-2026/raw/
```

---

### Step 2 – Transform

Uploading the file to Amazon S3 automatically triggers the Lambda function.

The Lambda function performs the following operations:

* Reads earthquake records from S3
* Removes invalid records
* Converts magnitude values into Decimal format
* Calculates earthquake risk level
* Adds processing timestamp
* Formats event time
* Generates ETL audit summary

Risk Levels

| Magnitude | Risk   |
| --------- | ------ |
| ≥ 5       | High   |
| ≥ 3       | Medium |
| < 3       | Low    |

---

### Step 3 – Load

The transformed records are stored in DynamoDB.

**Table Name**

```
clean_records
```

Partition Key

```
record_id
```

---

## CloudWatch Logging

Every Lambda execution generates an audit report containing:

* Total Records
* Inserted Records
* Rejected Records
* Processing Time

Example

```
Total Records : 212
Inserted Records : 212
Rejected Records : 0
```

---

## CI/CD Pipeline

Whenever code is pushed to the **main** branch:

```
Git Push
     │
     ▼
GitHub Actions
     │
     ▼
AWS CodePipeline
     │
     ▼
AWS CodeBuild
     │
     ▼
AWS Lambda Deployment
```

---

## GitHub Actions

The GitHub Actions workflow performs:

* Checkout repository
* Setup Python 3.11
* Install dependencies
* Validate Lambda syntax

---

## AWS CodeBuild

CodeBuild uses **buildspec.yml** to:

* Install Python runtime
* Validate Lambda code
* Generate build artifact

---

## AWS CodePipeline

Pipeline Stages

```
Source
   ↓
Build
   ↓
Deploy
```

Source → GitHub

Build → AWS CodeBuild

Deploy → AWS Lambda

---

## Project Structure

```
etl-s3-lambda-dynamodb/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── buildspec.yml
├── fetch_data.py
├── lambda_function.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Results

Successfully implemented:

* Serverless ETL Pipeline
* Amazon S3 Event Trigger
* AWS Lambda Data Processing
* DynamoDB Data Storage
* CloudWatch Logging
* GitHub Version Control
* GitHub Actions CI
* AWS CodeBuild
* AWS CodePipeline
* Automatic Lambda Deployment

---

## Author

**Smit Gadhiya**

MCA Student

GitHub: https://github.com/smitgadhiya017
