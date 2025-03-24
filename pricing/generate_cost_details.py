import requests
from azure.identity import DefaultAzureCredential
import time
from _process_csv import CSVProcessor

# Set up the client with Azure credentials
credential = DefaultAzureCredential()
access_token = credential.get_token("https://management.azure.com/.default").token

## Define the report generation parameters
subscription_id = '' # Set to your subscription ID; e.g. 697---------123
usage_start = "" # Set to the start date for the report: yyyy-mm-dd; e.g. 2025-03-21
usage_end = "" # Set to the end date for the report: yyyy-mm-dd; e.g. 2025-03-26
resource_name = "" # Set to the AOAI resource name to filter the report; e.g. oaimonitor001

# Define the API endpoint and headers
endpoint = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/generateCostDetailsReport?api-version=2024-08-01"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Define the request body
body = {
    "timePeriod": {
        "start": usage_start,
        "end": usage_end
    },
    "metric": "ActualCost"
}

# print(body)

# Initialize the report details variable
report_details = None

# Create the report request
response = requests.post(endpoint, headers=headers, json=body)
if response.status_code == 202:
    location = response.headers["Location"]
    retry_after = int(response.headers.get("Retry-After", 30))
    print(f"Report generation started. Polling status at: {location}")

    # Poll for the report status
    while True:
        time.sleep(retry_after)
        status_response = requests.get(location, headers=headers)
        if status_response.status_code == 200:
            report_details = status_response.json()
            print("Report is ready.")
            # print(report_details)
            break
        elif status_response.status_code == 202:
            retry_after = int(status_response.headers.get("Retry-After", 30))
            print(f"Report is still being generated. Retrying in {retry_after} seconds...")
        else:
            print(f"Failed to get report status: {status_response.status_code}")
            break
else:
    print(f"Failed to start report generation: {response.status_code}, {response.text}")

if report_details is not None:
    print(report_details)
else:
    print("Report details not available.")

## Extract the blob URL from the report details
blob_url = report_details["manifest"]["blobs"][0]["blobLink"]

# Download the CSV file
response = requests.get(blob_url)
csv_content = response.content.decode('utf-8')

# Save the CSV content to a local file
csv_filename = "downloaded_report.csv"
with open(csv_filename, mode='w', newline='') as file:
    file.write(csv_content)

print(f"Report downloaded to: {csv_filename}")

# Process the CSV file
processor = CSVProcessor(csv_filename)
processor.filter_resource_cost(resource_name)
