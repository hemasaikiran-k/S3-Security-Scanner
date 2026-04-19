import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
all_buckets = s3.list_buckets()['Buckets']

# Extensions often containing credentials or PII
SENSITIVE_EXTS = ('.env', '.sql', '.pem', '.key', '.config', '.bak', '.json', '.xml')

print(f"🚀 Starting Deep Scan on {len(all_buckets)} buckets...\n")

for bucket in all_buckets:
    name = bucket['Name']
    is_at_risk = False
    
    # Step 1: Rapid Risk Assessment
    try:
        s3.get_public_access_block(Bucket=name)
    except ClientError:
        is_at_risk = True

    if is_at_risk:
        print(f"🔓 BUCKET EXPOSED: {name}. Searching for sensitive data...")
        try:
            # Step 2: Content Enumeration (OSCP-style Recon)
            paginator = s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=name):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        if key.lower().endswith(SENSITIVE_EXTS):
                            print(f"   🚩 CRITICAL: Found {key} ({obj['Size']} bytes)")
                else:
                    print("   ℹ️ Bucket is open but empty.")
        except ClientError as e:
            print(f"   ⚠️ Enumeration failed: {e.response['Error']['Code']}")
    else:
        print(f"🔒 {name} is shielded. Skipping.")

print("\n--- Scan Complete ---")
