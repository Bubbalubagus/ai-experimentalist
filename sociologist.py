import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def create_form(json_data):
    """Create a Google Form based on provided JSON data."""
    form_data = {
        'info': {
            'title': json_data['title'],
            'description': json_data['description']
        },
        'items': []
    }

    for item in json_data['items']:
        if item['type'] == 'PARAGRAPH_TEXT':
            form_data['items'].append({
                'title': item['title'],
                'questionItem': {
                    'question': {
                        'required': True,
                        'textQuestion': {}
                    }
                }
            })
        elif item['type'] == 'LINEAR_SCALE':
            form_data['items'].append({
                'title': item['title'],
                'questionItem': {
                    'question': {
                        'required': True,
                        'scaleQuestion': {
                            'lowerBound': item['scale']['start'],
                            'upperBound': item['scale']['end']
                        }
                    }
                }
            })

    return form_data

def main():
    # Load credentials
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/drive']
    )
    creds = flow.run_local_server(port=0)
    
    # Connect to the Google Forms API
    service = build('forms', 'v1', credentials=creds)

    # Load your JSON data
    with open('form_data.json', 'r') as file:
        json_data = json.load(file)

    # Create form payload
    form_payload = create_form(json_data)
    
    # Create the form
    form = service.forms().create(body=form_payload).execute()
    print(f"Form created: {form['formId']}")
    print(f"Edit form URL: {form['editUrl']}")

if __name__ == "__main__":
    main()
