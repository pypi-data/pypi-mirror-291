import xml.etree.ElementTree as ET
from collections import OrderedDict
import time
import json 

def create_bids_metadata(connection, project, subject, session):
    """
    Create BIDS metadata for the given session and upload it to XNAT.

    Args:
    - connection (XnatClient): An XnatClient object.
    - project (pyxnat.core.resources.Project): The project to upload the data to.
    - subject (pyxnat.core.resources.Subject): The subject to upload the data to.
    - session (pyxnat.core.resources.Experiment): The session to upload the data to
    """

    BIDSVERSION = "1.3.0"
    
    # Access the 'BIDS' resource under the session
    bids_resource = session.resource('BIDS')

    # Check if 'BIDS' resource exists, delete and recreate if needed
    if bids_resource.exists():
        bids_resource.delete()

    bids_resource.create()
    
    # Fetch project metadata
    project_xml = project.get()

    # Define namespace map for XML parsing
    namespace_map = {'xnat': 'http://nrg.wustl.edu/xnat'}

    # Parse XML data
    root = ET.fromstring(project_xml)
    for prefix, uri in namespace_map.items():
        ET.register_namespace(prefix, uri)

    # Extract project data using the namespace
    project_name = root.find('.//xnat:name', namespaces=namespace_map).text

    # Extract PI data if available
    pi_elem = root.find('.//xnat:PI', namespaces=namespace_map)
    pi_firstname = pi_elem.find('.//xnat:firstname', namespaces=namespace_map).text if pi_elem is not None else None
    pi_lastname = pi_elem.find('.//xnat:lastname', namespaces=namespace_map).text if pi_elem is not None else None

    # Construct BIDS dataset description
    dataset_description = OrderedDict()
    dataset_description['Name'] = project_name
    dataset_description['BIDSVersion'] = BIDSVERSION

    inv_names = []

    # Extract investigator data if available
    for inv_elem in root.findall('.//xnat:investigator', namespaces=namespace_map):
        inv_firstname = inv_elem.find('.//xnat:firstname', namespaces=namespace_map).text
        inv_lastname = inv_elem.find('.//xnat:lastname', namespaces=namespace_map).text
        inv_names.append(f"{inv_firstname} {inv_lastname}")

    # Add PI to the list if PI data is available
    if pi_firstname is not None and pi_lastname is not None:
        pi_name = f"{pi_firstname} {pi_lastname}"
        inv_names.insert(0, f"{pi_name} (PI)")

    if inv_names:
        dataset_description['Authors'] = inv_names

    dataset_description['DatasetDOI'] = f'https://xnat.abudhabi.nyu.edu/data/experiments/{session.id()}'

    # Convert dataset_description to JSON and upload to XNAT
    json_data = json.dumps(dataset_description, indent=4)
    bids_resource.file('dataset_description.json').insert(
        json_data,
        content="BIDS",
        format='BIDS',
        tags='BIDS',
    )

    # Create CHANGES file content
    changes_content = f"1.0 {time.strftime('%Y-%m-%d')}\n\n - Initial release."

    readme_content = '''Converted from HCPD Nifty file to BIDS structure. 
        All HCP data were downloaded from ConnectomeDB. These data are already converted from DICOM to NIFTI, but the file naming and folder structure are not as specified for BIDS.
        The current folder contains the converted HCPD NIFTI data to the BIDS structure'''

    # Upload CHANGES file to XNAT
    bids_resource.file('CHANGES').insert(
        changes_content,
        content="BIDS",
        format='BIDS',
        tags='BIDS',
    )

    # Upload README file to XNAT
    bids_resource.file('README').insert(
        readme_content,
        content="BIDS",
        format='BIDS',
        tags='BIDS',
    )
