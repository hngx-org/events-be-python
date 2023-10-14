from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Define the scope for Gmail API access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRET_FILE = 'client_secret_188658735176-jhpmkjvo54mhdd0pqdnkcqvtc22oqidk.apps.googleusercontent.com.json'

# Create a flow to obtain the access token
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

# Print the access token
print(f"Access Token: {credentials.token}")
