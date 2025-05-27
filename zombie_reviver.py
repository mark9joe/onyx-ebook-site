from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file('credentials.json')
analytics = build('analyticsreporting', 'v4', credentials=credentials)

response = analytics.reports().batchGet(
    body={
        'reportRequests': [{
            'metrics': [{'expression': 'ga:pageviews'}],
            'dimensions': [{'name': 'ga:pagePath'}],
            'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}],
            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'yesterday'}]
        }]
    }
).execute()

for report in response['reports']:
    for row in report['data']['rows']:
        if row['metrics'][0]['values'][0] < 100:  # Low traffic
            update_content(row['dimensions'][0])  # Your CMS API call
