import os
import json
import sys 

def analyze_directory_structure(base_dir):
    directory_map = {}

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        relative_dir = os.path.relpath(root, base_dir)
        directory_map[relative_dir] = files

    return directory_map

def build_map(session, session_data):
    sub_ses_dirs = []
    for root, dirs, files in os.walk(session_data):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if os.path.basename(root).startswith('ses-') and os.path.basename(os.path.dirname(root)).startswith('sub-'):
            sub_ses_dirs.append(root)
    
    complete_map = {}
    for sub_ses_dir in sub_ses_dirs:
        sub_ses_map = analyze_directory_structure(sub_ses_dir)
        complete_map.update({os.path.relpath(os.path.join(sub_ses_dir, key), session_data): value for key, value in sub_ses_map.items()})
    
    bids_resource = session.resource('BIDS')
    if not bids_resource.exists():
        sys.exit(1)

    complete_map_json = json.dumps(complete_map, indent=4)
    bids_resource.file('BIDS_map.json').insert(
        complete_map_json,
        content="BIDS_map",
        format='BIDS_map',
        tags='BIDS_map',
    )
