from google.oauth2 import service_account

client_file = 'sa-mock-ai-interviewer'
credentials = service_account.Credentials.from_service_account_file(client_file + '.json')