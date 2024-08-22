import os
import json
import sys 

def analyze_directory_structure(directory, base_dir):
    directory_map = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        relative_root = os.path.relpath(root, base_dir)
        if files:
            directory_map[relative_root] = files
    return directory_map

def build_map(session, session_data):
    print(session_data)
    sub_ses_dirs = []
    
    for root, dirs, files in os.walk(session_data):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if os.path.basename(root).startswith('ses-') and os.path.basename(os.path.dirname(root)).startswith('sub-'):
            sub_ses_dirs.append(root)
    
    complete_map = {}
    for sub_ses_dir in sub_ses_dirs:
        sub_ses_map = analyze_directory_structure(sub_ses_dir, session_data)
        
        for key, value in sub_ses_map.items():
            full_key = os.path.join(os.path.basename(os.path.dirname(sub_ses_dir)), os.path.basename(sub_ses_dir), key)
            complete_map[full_key] = value
    
    bids_resource = session.resource('BIDS')
    if not bids_resource.exists():
        print(f'BIDS resource does not exist for session {session.label}')
        return

    complete_map_json = json.dumps(complete_map, indent=4)

    bids_resource.file('BIDS_map.json').insert(
        complete_map_json,
        content="BIDS_map",
        format='BIDS_map',
        tags='BIDS_map',
    )
