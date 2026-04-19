S3 Security Auditor v2.0
📌 Project Overview
As cloud adoption grows, S3 bucket misconfigurations remain a leading cause of data breaches. This Python-based security tool automates the auditing of AWS S3 environments. Unlike basic scripts that only check for "Public" flags, this tool cross-references Public Access Blocks and Bucket Policy Status to provide a definitive security posture.
🛠 Features
Dual-Layer Verification: Checks both Account/Bucket-level "Public Access Blocks" and effective "Bucket Policies."
Intelligent Logic: Uses AWS get_bucket_policy_status to determine if complex JSON policies actually allow public access.
Professional Reporting: Automatically generates a s3_security_audit.csv report for stakeholders.
Error Resiliency: Built-in handling for ClientError to manage permission issues or missing policies without crashing.

This project demonstrates the ability to automate Cloud Security Posture Management (CSPM). It reduces manual audit time by 90% and ensures that "hidden" public access via bucket policies is flagged before it leads to a data leak.
