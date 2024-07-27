'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import analysis_network_centrality
import analysis_similar_actors_genre
import requests

# Ingest and save the imbd_movies dataset
def download_dataset(url, path):
    """
    Download dataset from a given URL and saves it
    
    Parameters:
    url (str): The URL to download the dataset from.
    path (str): The local file path to save the downloaded dataset.

    Returns:
    None
    """
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)


# Call functions / instanciate objects from the two analysis .py files
def main():
    # URL of the dataset
    url = "https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json"
    # Save path
    path = "data/imdb_movies_2000to2022.prolific.json"
    download_dataset(url, path)
    analysis_network_centrality.run_analysis(path) 

if __name__ == "__main__":
    main()