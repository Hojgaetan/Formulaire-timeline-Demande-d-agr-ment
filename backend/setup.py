#!/usr/bin/env python3
"""
Setup script for the backend application
"""
import os
import shutil
import sys
from database import init_db

def create_static_dirs():
    """Create static directories if they don't exist"""
    print("Creating static directories...")
    
    # Create static directory if it doesn't exist
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Created directory: {static_dir}")
    
    # Create subdirectories
    subdirs = ['css', 'js', 'images', 'vendor', 'fonts']
    for subdir in subdirs:
        subdir_path = os.path.join(static_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
            print(f"Created directory: {subdir_path}")

def copy_static_files():
    """Copy static files from project root to backend/static"""
    print("Copying static files...")
    
    # Get project root directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    
    # Define directories to copy
    dirs_to_copy = ['css', 'js', 'images', 'vendor', 'fonts']
    
    for dir_name in dirs_to_copy:
        src_dir = os.path.join(project_root, dir_name)
        dest_dir = os.path.join(backend_dir, 'static', dir_name)
        
        if os.path.exists(src_dir):
            print(f"Copying {dir_name} files...")
            
            # Remove destination directory if it exists
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            
            # Copy directory
            shutil.copytree(src_dir, dest_dir)
            print(f"Copied {dir_name} files to {dest_dir}")
        else:
            print(f"Warning: Source directory {src_dir} not found")

def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    
    return True

def main():
    """Main function to run setup"""
    print("Starting setup...\n")
    
    # Create static directories
    create_static_dirs()
    
    # Copy static files
    copy_static_files()
    
    # Initialize database
    if initialize_database():
        print("\nSetup completed successfully!")
        print("\nYou can now run the application with:")
        print("  python app.py")
    else:
        print("\nSetup failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())