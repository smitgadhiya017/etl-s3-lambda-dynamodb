# ETL Pipeline using AWS S3, Lambda, DynamoDB, GitHub Actions & CodePipeline

## Project Overview

This project implements a serverless ETL (Extract, Transform, Load) pipeline on AWS.

The pipeline automatically detects the uploaded file type (JSON, CSV, or XML), triggers the corresponding AWS Lambda parser, transforms earthquake data, and stores the cleaned records into Amazon DynamoDB.

The complete deployment is automated using GitHub Actions, AWS CodeBuild, and AWS CodePipeline.

---

# Architecture

GitHub Repository
        │
        ▼
GitHub Actions (CI)
        │
        ▼
AWS CodePipeline
        │
        ▼
AWS CodeBuild
        │
        ▼
AWS Lambda Deployment
        │
        ▼
Amazon S3 (Upload File)
        │
        ▼
Specific Lambda Parser
(JSON / CSV / XML)
        │
        ▼
Transform Data
        │
        ▼
Amazon DynamoDB
        │
        ▼
CloudWatch Logs

---

# Features

- Serverless ETL Pipeline
- Automatic parser selection based on uploaded file type
- Supports JSON files
- Supports CSV files
- Supports XML files
- Data validation
- Risk level calculation
- CloudWatch logging
- DynamoDB storage
- CI/CD using GitHub Actions
- Automatic deployment using AWS CodePipeline
- Build automation using AWS CodeBuild

---

# Technologies Used

- Python 3.11
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- AWS CloudWatch
- AWS CodeBuild
- AWS CodePipeline
- GitHub Actions
- Git
- JSON
- CSV
- XML

---

# Project Structure

```
etl-s3-lambda-dynamodb/

│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── sample_data/
│   ├── sample_raw_data.json
│   ├── sample_raw_data.csv
│   └── sample_rwa_data.xml
│
├── lambda_function.py
├── lambda_json.py
├── lambda_csv.py
├── lambda_xml.py
│
├── fetch_data.py
├── buildspec.yml
├── requirements.txt
├── README.md
│
└── screenshots/
```

---

# ETL Workflow

## Step 1

Earthquake data is uploaded into Amazon S3.

Example:

```
raw/sample_raw_data.json
raw/sample_raw_data.csv
raw/sample_rwa_data.xml
```

---

## Step 2

Amazon S3 automatically triggers the appropriate Lambda function.

| File Type | Triggered Lambda |
|------------|-----------------|
| JSON | earthquake-json-parser |
| CSV | earthquake-csv-parser |
| XML | earthquake-xml-parser |

---

## Step 3

The Lambda function:

- Reads the file
- Validates records
- Calculates Risk Level
- Cleans the data
- Creates structured output

---

## Step 4

Cleaned data is stored in Amazon DynamoDB.

Each record contains:

- record_id
- place
- magnitude
- risk_level
- event_time
- processed_at
- file_type

---

# Risk Level Logic

| Magnitude | Risk Level |
|------------|------------|
| < 3 | Low |
| 3 – 4.9 | Medium |
| ≥ 5 | High |

---

# Supported File Types

## JSON

```
sample_raw_data.json
```

---

## CSV

```
sample_raw_data.csv
```

---

## XML

```
sample_rwa_data.xml
```

---

# CI/CD Pipeline

This project uses GitHub Actions and AWS CodePipeline.

Workflow:

Developer Push

↓

GitHub Actions

↓

AWS CodePipeline

↓

AWS CodeBuild

↓

AWS Lambda Deployment

---

# AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon DynamoDB
- AWS IAM
- AWS CloudWatch
- AWS CodeBuild
- AWS CodePipeline

---

# Sample DynamoDB Record

```json
{
  "record_id": "ak20260001",
  "place": "California",
  "magnitude": 5.4,
  "risk_level": "High",
  "event_time": "2026-06-30 10:20:30 UTC",
  "processed_at": "2026-06-30 10:22:15 UTC",
  "file_type": "json"
}
```

---

# Screenshots

Add screenshots inside the `screenshots/` folder.

Recommended screenshots:

- GitHub Repository
- GitHub Actions Success
- AWS CodePipeline Success
- AWS CodeBuild Success
- Lambda Functions
- S3 Bucket
- DynamoDB Table
- CloudWatch Logs
- JSON Parser Logs
- CSV Parser Logs
- XML Parser Logs

---

# Future Enhancements

- Support Excel files
- Support Parquet format
- SNS Email Notification
- EventBridge Integration
- Glue Data Catalog
- Athena Queries
- S3 Versioning
- Terraform Deployment
- Docker Support

---

# Author

**Smit Gadhiya**

MCA Student

Data Engineering Enthusiast

GitHub:
https://github.com/smitgadhiya017

---
