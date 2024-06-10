import googleapiclient.discovery

def run_apps_script(contact_info, right_column_content):
    """Executes the Apps Script function and passes the contact info and right column content."""
    service = googleapiclient.discovery.build('script', 'v1', credentials=creds) # Ensure you've set up your credentials (creds)

    request = {
        'function': 'createContactInfoLayout',  
        'parameters': [contact_info, right_column_content]
    }

    response = service.scripts().run(scriptId=SCRIPT_ID, body=request).execute() # Replace SCRIPT_ID with your script's ID

    if 'error' in response:
        raise Exception(response['error']['message'])

# Example Contact Info
my_contact_info = [
    "COLTON",
    "DATA ANALYST",
    "______", // Space 
    " ", // Space
    "Colton Robbins",
    "Snohomish, WA USA",
    "206-552-4365",
    "coltonrobbins73@gmail.com",
    "______", // Space 
    " ", // Space
    "portfolio-cmr.github.io/Directory",
    "linkedin.com/in/colton-robbins73",
    "github.com/coltonrobbins73"
]

# Example Right Column Content
my_right_column_content = "This is some text for the right column of the resume."

run_apps_script(my_contact_info, my_right_column_content)
