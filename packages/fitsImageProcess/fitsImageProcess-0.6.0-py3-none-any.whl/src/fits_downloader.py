# fits_downloader.py
import os

from astroquery.gemini import Observations


class FITSDownloader:

    def download(self, data_url, download_path):
        """
        Download an image from a specified URL.

        Parameters:
        data_url (str): URL of the image to download.
        download_path (str): Path where the image will be downloaded.

        Returns:
        str: Path of the downloaded file.
        """
        # Extract the file name from the URL
        file_name = data_url.split("/")[-1]

        # Create the directory if it doesn't exist
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Download the file if it doesn't exist locally
        if not os.path.exists(os.path.join(download_path, file_name)):
            Observations.download_file(data_url, local_path=os.path.join(download_path, file_name))
            print("The file has been downloaded")

        # Return the path of the downloaded file
        return os.path.join(download_path, file_name)