import json
import os
import glob
import datetime

def load_metadata(result_folder='./results'):
    """Load metadata from JSON files in the results folder."""
    print("Starting metadata loading...")
    print(f"Looking for JSON files in: {os.path.abspath(result_folder)}")
    
    json_files = glob.glob(os.path.join(result_folder, '*.json'))
    print(f"Found {len(json_files)} JSON files")
    
    metadata_list = []
    
    for file_path in json_files:
        print(f"Processing file: {file_path}")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                metadata = data.get('metadata', {})
                if metadata:
                    metadata_entry = process_metadata(metadata, file_path)
                    metadata_list.append(metadata_entry)
                    print(f"Successfully processed metadata for {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    print(f"Total metadata entries loaded: {len(metadata_list)}")
    return metadata_list

def process_metadata(metadata, file_path):
    """Process individual metadata entries."""
    run_date_str = metadata.get('run_date', '')
    try:
        run_date = datetime.datetime.strptime(run_date_str, '%Y-%m-%d').isoformat()
    except ValueError:
        run_date = run_date_str

    try:
        run_duration = float(metadata.get('run_duration', ''))
    except ValueError:
        run_duration = 0

    return {
        'uuid': metadata.get('uuid', ''),
        'project_name': metadata.get('name', ''),
        'run_date': run_date,
        'run_by': metadata.get('run_by', ''),
        'run_time': metadata.get('run_time', ''),
        'run_duration': run_duration,
        'description': metadata.get('description', ''),
        'file_path': file_path
    } 