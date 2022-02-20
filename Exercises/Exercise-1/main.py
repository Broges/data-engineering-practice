from xmlrpc.client import Boolean
import requests
import os
import zipfile
from io import BytesIO

class Downloader():

    download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

    def __init__(self) -> None:
        pass

    
    def get_response(self, uri):
        # grabs response info and assigns to attributes
        self.response = requests.get(uri)
        self.status_code = self.response.status_code
        self.content_type = self.response.headers.get('content-type')
        self.headers = self.response.headers
        self.content = self.response.content
        self.file_name = uri.split('/')[-1].replace('.zip','.csv')


    def verify_uri(self) -> Boolean:
        valid_uri = True

        if self.status_code != 200:
            print(f'Bad response, response returned {self.status_code}')
            valid_uri = False
        else:
            print(f'status code: {self.status_code}')

        # all uris should be zip files
        if self.content_type != 'application/zip':
            print(f'Bad content type, {self.content_type}')
            valid_uri = False

        return valid_uri


    @staticmethod
    def verify_down_dir_exists() -> None:
        if not os.path.isdir('downloads'):
            os.mkdir('downloads')

    def unzip_file(self) -> None:
        zip_file = zipfile.ZipFile(BytesIO(self.content))
        print(f'Extracting {self.file_name}')
        zip_file.extract(self.file_name, 'downloads')

        

def main():
    downloader = Downloader()
    downloader.verify_down_dir_exists()
    for uri in downloader.download_uris:
        downloader.get_response(uri)
        if downloader.verify_uri():
            downloader.unzip_file()
        else:
            print('invalid uri. skipping...')


if __name__ == '__main__':
    main()
