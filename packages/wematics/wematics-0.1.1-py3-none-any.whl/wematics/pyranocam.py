import requests
import datetime
import os
from tqdm import tqdm


class Pyranocam:
    def __init__(self, api_key):
        self.base_url = "http://wematics.cloud"
        self.api_key = api_key

    def _make_request(self, endpoint: str, params=None):
        """Makes a request to the API with error handling."""
        url = f"{self.base_url}{endpoint}"
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(url, params=params)

        # Raise an exception for bad status codes
        response.raise_for_status()
        return response.json()

    def list_variables(self):
        """Lists all available variables."""
        return self._make_request("/variables")

    def list_dates(self, variable):
        """Lists all available dates for a given variable."""
        return self._make_request(f"/dates/{variable}")

    def list_files(self, variable, date):
        """Lists all available files for a given variable and date."""
        return self._make_request(f"/files/{variable}/{date}")
    
    def download_image(self, variable, file_timestamp, download_path=""):
        """Downloads a single JPG file."""
        date = file_timestamp.split('_')[0] 
        if variable.upper() == "HDR": 
            ext = '.jpg'
        elif variable.upper() == "MASK":
            ext = '_mask.png'
        elif variable.upper() == "RGB":
            ext = '_rgb.jpg'
        file_path_on_server = f"{variable}/{date}/{file_timestamp}{ext}"
        
        url = f"{self.base_url}/download/{file_path_on_server}"
        print(url)
        self._download_file(url, f"{file_timestamp}{ext}", download_path)

    def download_csv_file(self, variable, file_timestamp, download_path=""):
        """Downloads a single CSV file."""
        if variable.upper() == 'CC':
            prefix = 'cloud_cover'  
            variable = 'CC'
        if variable.upper() == 'GHI':
            prefix = 'ghi'  
            variable = 'ghi'
        date = file_timestamp.split('_')[0]
        file_path_on_server = f"{variable}/{date}/{prefix}_{date}.csv"
        url = f"{self.base_url}/download/{file_path_on_server}"
        print(url)
        self._download_file(url, f"{prefix}_{date}.csv", download_path)

    def _download_file(self, url, file_name, download_path=""):
        """Downloads a file from a given URL (helper function)."""
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params, stream=True)

        if response.status_code == 200:
            file_path = os.path.join(download_path, file_name)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=4096), 
                                  total=total_size // 4096, 
                                  unit='KB', 
                                  desc=f"Downloading {file_name}"):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Error downloading {file_name}: {response.text}")


    def download_images_in_range(self, variable, start_datetime, end_datetime, download_path="."): 
        """Downloads files for a variable within a datetime range with a progress bar."""
        start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d_%H_%M_%S")
        end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d_%H_%M_%S")

        # Get file list for the relevant dates
        all_files = []
        current_date = start_datetime.date()
        while current_date <= end_datetime.date():
            date_str = current_date.strftime("%Y-%m-%d")
            files = self.list_files(variable, date_str)['files']
            all_files.extend(files)
            current_date += datetime.timedelta(days=1) 

        # Filter files based on the time range
        filtered_files = []
        for file_name in all_files:
            # Extract timestamp from filename (assuming file_name format is consistent)
            file_timestamp = '_'.join(file_name.split('_')[:4]).replace('.jpg', '') 
            file_datetime = datetime.datetime.strptime(file_timestamp, "%Y-%m-%d_%H_%M_%S")
            if start_datetime <= file_datetime <= end_datetime:
                filtered_files.append(file_timestamp)  # Append timestamp to the list

        total_files = len(filtered_files)

        # Download the filtered files using the download_file method
        for file_timestamp in tqdm(filtered_files, desc="Downloading", unit="file"):
            self.download_image(variable, file_timestamp, download_path) 
        