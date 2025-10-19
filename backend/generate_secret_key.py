"""
Generate a secure SECRET_KEY for production deployment.
Run this script and copy the output to your Render environment variables.
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("\n" + "="*60)
    print("🔐 Generated SECRET_KEY for production:")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("Copy this value to Render environment variables:")
    print("SECRET_KEY=" + secret_key)
    print("="*60 + "\n")
