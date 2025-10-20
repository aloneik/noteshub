"""
Script to create an admin user.
Usage: python create_admin.py
"""
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.db import crud


async def create_admin():
    """Create an admin user."""
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    
    async with SessionLocal() as db:
        # Check if user exists
        existing_user = await crud.get_user_by_username(db, username)
        if existing_user:
            print(f"User '{username}' already exists.")
            
            # Ask if we should make them admin
            make_admin = input("Make this user an admin? (y/n): ").strip().lower()
            if make_admin == 'y':
                existing_user.is_admin = True
                await db.commit()
                print(f"✓ User '{username}' is now an admin!")
            else:
                print("No changes made.")
            return
        
        # Create new admin user
        user = await crud.create_user(db, username, password)
        user.is_admin = True
        await db.commit()
        await db.refresh(user)
        
        print(f"✓ Admin user created successfully!")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Admin: {user.is_admin}")


if __name__ == "__main__":
    asyncio.run(create_admin())
