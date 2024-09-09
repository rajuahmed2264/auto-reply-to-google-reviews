from google.analytics.data_v1beta import BetaAnalyticsDataClient, RunReportRequest
import pandas as pd
import numpy as np

# Replace with your actual credentials file path and GA4 property ID
credentials_path = 'creds.json'
property_id = '420225925'

# Initialize the Google Analytics Data API client without passing credentials parameter
client = BetaAnalyticsDataClient()

# Define a function to format the report response into a Pandas DataFrame
def format_report(request):
    response = client.run_report(request)
    
    # Row index
    row_index_names = [header.name for header in response.dimension_headers]
    row_header = []
    for i in range(len(row_index_names)):
        row_header.append([row.dimension_values[i].value for row in response.rows])

    row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names=np.array(row_index_names))
    
    # Row flat data
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')), 
                          index=row_index_named, columns=metric_names)
    return output

# Example request to get sessions and pageviews for the last 30 days for a specific property ID
request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[{"start_date": "30daysAgo", "end_date": "yesterday"}],
    metrics=[{"name": "sessions"}, {"name": "pageviews"}],
    dimensions=[{"name": "date"}],
)

# Call the format_report function with the request
result_df = format_report(request)

# Display the resulting DataFrame
print(result_df)
