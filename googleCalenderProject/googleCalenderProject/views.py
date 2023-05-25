from django.shortcuts import redirect
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

def GoogleCalendarInitView(request):
    # Step 1: Prompt user for credentials
    flow = Flow.from_client_secrets_file(
        '/Users/bhavy/Downloads/client_secret.json',
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    return redirect(authorization_url)

def GoogleCalendarRedirectView(request):
    # Step 2: Handle redirect request
    code = request.GET.get('code', None)
    if code:
        flow = Flow.from_client_secrets_file(
            '/Users/bhavy/Downloads/client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Use the credentials to get a list of events from the user's calendar
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])

        # Handle the events as required
        # ...

        return HttpResponse(events)
    else:
        return HttpResponse('Error: Code not provided')
