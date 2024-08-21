"""Small script that downloads the air archive data from the AGAGE website.

Make sure to set the correct local_folder to save the data.
"""

from bs4 import BeautifulSoup
import requests
from pathlib import Path

data_folders = [
    "gc-md",
    "gc-ms",
    "gc-ms-medusa",
    "picarro",
]
local_folder = Path("agage_air_archive")

# Base URL of the website
base_url = "https://agage2.eas.gatech.edu/data_archive/agage/"


if __name__ == "__main__":

    for folder in data_folders:

        folder_url = base_url + folder + "/event/"

        response = requests.get(folder_url)
        # print the response
        # Parse the html content
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            # Name of the station subfolder
            href = link.get("href")

            # Skip other links
            if not href.endswith("/"):
                continue
            if href.startswith("/"):
                continue

            site_link = folder_url + href + "netcdf/"

            sub_response = requests.get(site_link)
            # Parse the html content
            sub_soup = BeautifulSoup(sub_response.text, "html.parser")

            print("Acessing: ", site_link)
            for sub_link in sub_soup.find_all("a"):

                # Name of the station subfolder
                href = sub_link.get("href")
                # Skip other links
                if not href.endswith(".nc"):
                    continue
                if href.startswith("/"):
                    continue

                print("Downloading: ", href)
                download_link = site_link + href

                # Download the file
                response = requests.get(download_link)
                file_path = local_folder / href
                with open(file_path, "wb") as file:
                    file.write(response.content)
