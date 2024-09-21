import requests
from bs4 import BeautifulSoup

# URL for the GEM report page
GEM_REPORTS_URL = "https://gemconsortium.org/report"

# Function to fetch the first file ID and construct the download URL
def fetch_first_download_url():
    # Send a GET request to the reports page
    response = requests.get(GEM_REPORTS_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first button with the 'file' attribute
    first_button = soup.find('button', class_='downloadaction', file=True)
    if not first_button:
        raise Exception("No download buttons found on the page.")

    # Extract the file ID from the 'file' attribute
    file_id = first_button['file']

    # Construct the download URL using the file ID

    download_url = f"https://gemconsortium.org/file/open?fileId={file_id}"
    print(f"Downloading {download_url}")

    return download_url

# Function to download the PDF from the extracted download URL
def download_gem_report(download_url, output_path="gem_report.pdf"):
    # Send a request to download the PDF
    response = requests.get(download_url)
    if response.status_code == 200:
        # Write the content to a file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Report downloaded successfully: {output_path}")
    else:
        raise Exception(f"Failed to download the report. Status code: {response.status_code}")

"""# Main process
if __name__ == "__main__":
    try:
        # Step 1: Fetch the first download URL
        download_url = fetch_first_download_url()

        # Step 2: Download the report using the constructed URL
        download_gem_report(download_url, output_path="gem_report.pdf")
    except Exception as e:
        print(f"An error occurred: {e}")
"""