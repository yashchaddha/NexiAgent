#!/usr/bin/env python3
"""
Database initialization script for ISO 27001:2022 Auditor
This script creates the database and tables if they don't exist.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
from database import engine, Base
from models import User, UserConversation
import logging

# Load environment variables from the root directory
load_dotenv("../.env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create the database if it doesn't exist"""
    
    # Get the POSTGRES_URI from environment
    postgres_uri = os.getenv('POSTGRES_URI')
    if not postgres_uri:
        print("❌ POSTGRES_URI environment variable not found")
        return False
    
    try:
        # Parse the URI to get connection parameters
        # Format: postgresql://user:password@host:port/database
        uri_parts = postgres_uri.replace('postgresql://', '').split('@')
        if len(uri_parts) != 2:
            print("❌ Invalid POSTGRES_URI format")
            return False
        
        credentials_part = uri_parts[0]
        host_part = uri_parts[1]
        
        username = credentials_part.split(':')[0]
        password = credentials_part.split(':')[1]
        
        host_port_db = host_part.split('/')
        if len(host_port_db) != 2:
            print("❌ Invalid POSTGRES_URI format")
            return False
        
        host_port = host_port_db[0]
        database = host_port_db[1].split('?')[0]  # Remove query parameters
        
        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host = host_port
            port = '5432'
        
        # Database connection parameters
        db_params = {
            'host': host,
            'port': port,
            'user': username,
            'password': password,
            'database': 'postgres'  # Connect to default postgres database first
        }
        
        # Connect to PostgreSQL server
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{database}'...")
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"Database '{database}' created successfully!")
        else:
            print(f"Database '{database}' already exists.")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def init_database():
    """Initialize the database with all models"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # Log the tables that were created
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def main():
    """Main function to initialize the database"""
    print("🚀 Initializing ISO 27001:2022 Auditor Database...")
    
    # Step 1: Create database
    if create_database():
        print("✅ Database creation completed")
    else:
        print("❌ Database creation failed")
        return
    
    # Step 2: Create tables
    if init_database():
        print("✅ Table creation completed")
    else:
        print("❌ Table creation failed")
        return
    
    print("🎉 Database initialization completed successfully!")
    print("\nNext steps:")
    print("1. Make sure PostgreSQL is running")
    print("2. Your .env file is already configured with POSTGRES_URI")
    print("3. Run the authentication server: python login.py")
    print("4. Test the endpoints with the provided examples")

if __name__ == "__main__":
    main()
