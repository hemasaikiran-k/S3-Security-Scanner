import boto3
import csv
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
all_buckets = s3.list_buckets()['Buckets']

report_data = []

print(f"Scanning {len(all_buckets)} buckets...\n")

for bucket in all_buckets:
    name = bucket['Name']
    status = {"Name": name, "PublicBlock": "Missing", "PolicyStatus": "Safe"}
    
    ### 1. Check Public Access Block (Your original check)
    try:
        s3.get_public_access_block(Bucket=name)
        status["PublicBlock"] = "✅ Locked"
    except ClientError:
        status["PublicBlock"] = "❌ UNLOCKED"

    ### 2. Check Bucket Policy for Public Access
    try:
        policy_status = s3.get_bucket_policy_status(Bucket=name)
        if policy_status['PolicyStatus']['IsPublic']:
            status["PolicyStatus"] = "⚠️ PUBLIC POLICY"
    except ClientError as e:
        ### NoSuchBucketPolicy means it's private by default
        status["PolicyStatus"] = "Safe (No Policy)"

    report_data.append(status)
    print(f"Bucket: {name:<30} | Block: {status['PublicBlock']:<10} | Policy: {status['PolicyStatus']}")

### 3. Export to CSV (Professional reporting)
with open('s3_security_audit.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "PublicBlock", "PolicyStatus"])
    writer.writeheader()
    writer.writerows(report_data)

print("\nScan complete. Results saved to 's3_security_audit.csv'.")
