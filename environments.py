#!/usr/bin/env python3
import aws_cdk as cdk
from dotenv import load_dotenv
load_dotenv(override=True)
import os

software_engineering = {
    "ROOT": cdk.Environment(account=os.getenv("ROOT_ACCOUNT"), region="us-east-1"),
    "DEV": cdk.Environment(account=os.getenv("DEV_ACCOUNT"), region="us-east-1"),
}