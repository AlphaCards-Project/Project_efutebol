import psycopg2
import sys

project_ref = "egydaqgczfhrpqejnhtp"
password = "Fr33D0m4AllC0nFiD3nc3"
db_name = "postgres"
user = f"postgres.{project_ref}"

# Common regions for Supabase
regions = [
    "us-east-1", 
    "sa-east-1", 
    "eu-central-1", 
    "ap-southeast-1", 
    "us-west-1", 
    "ap-northeast-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "ca-central-1",
    "ap-south-1",
    "ap-southeast-2"
]

print(f"Testing connection for project: {project_ref}")
print(f"User: {user}")

for region in regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    print(f"\n--- Testing Region: {region} ({host}) ---")
    
    try:
        # Try Port 5432 (Session Mode)
        print(f"Attempting connection on port 5432 (Session Mode)...")
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name,
            port=5432,
            sslmode="require",
            connect_timeout=5
        )
        print(f"✅ SUCCESS! Connected to {region} on port 5432")
        conn.close()
        sys.exit(0)
    except psycopg2.OperationalError as e:
        msg = str(e).strip()
        print(f"❌ Failed: {msg}")
        if "password authentication failed" in msg:
            print("⚠️  PASSWORD INCORRECT (but region seems correct)")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

print("\nCould not connect to any region.")
