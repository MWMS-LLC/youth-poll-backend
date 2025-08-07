#!/usr/bin/env python3
"""
Script to add site column to CSV files for multi-site support
"""

import pandas as pd
from pathlib import Path
import sys

def add_site_column(csv_file: Path, site: str):
    """Add site column to CSV file"""
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        
        # Add site column if it doesn't exist
        if 'site' not in df.columns:
            df['site'] = site
            print(f"✅ Added 'site' column with value '{site}' to {csv_file.name}")
        else:
            print(f"⚠️  'site' column already exists in {csv_file.name}")
        
        # Save back to CSV
        df.to_csv(csv_file, index=False)
        print(f"💾 Saved updated {csv_file.name}")
        
    except Exception as e:
        print(f"❌ Error processing {csv_file.name}: {e}")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python add_site_to_csv.py <site_name>")
        print("Example: python add_site_to_csv.py youth")
        sys.exit(1)
    
    site = sys.argv[1]
    data_dir = Path(__file__).parent.parent / 'data'
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        sys.exit(1)
    
    csv_files = ['categories.csv', 'questions.csv', 'options.csv', 'blocks.csv']
    
    print(f"🔧 Adding site column with value '{site}' to CSV files...")
    
    for csv_file in csv_files:
        file_path = data_dir / csv_file
        if file_path.exists():
            add_site_column(file_path, site)
        else:
            print(f"⚠️  File not found: {csv_file}")
    
    print(f"\n🎉 Done! All CSV files now have site='{site}'")
    print("\n📝 Next steps:")
    print("1. Edit the CSV files in Excel to add different content for different sites")
    print("2. For example, add rows with site='teen' for teen site content")
    print("3. Run: python import_setup.py to import the updated data")

if __name__ == "__main__":
    main()
