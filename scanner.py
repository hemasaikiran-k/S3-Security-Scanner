import boto3

s3 = boto3.client('s3')

all_buckets = s3.list_buckets()['Buckets']

print("Starting Security Check...")

for bucket in all_buckets:
    name = bucket['Name']
    
    try:
        s3.get_public_access_block(Bucket=name)
        print(f"✅ {name} is LOCKED (Safe)")
    except:
        print(f"❌ ALERT: {name} is UNLOCKED (Public Data Leak!)")
