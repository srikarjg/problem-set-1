'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import json
import pandas as pd
import collections
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances
import datetime

def analysis(filepath, query):
        """Reads JSON file a builds dataframe, calculating cosine and Euclidean distances between query actor and other actors.

        Parameters:
            filepath (str): Path to JSON file containing movie data.
            query (str): Name of actor for query
            
        Returns: 
        none
        """
        actor_genre_count = {}
        
        #Read JSON file through each line
        with open(filepath, 'r') as file:
                for line in file:
                        this_movie = json.loads(line)
                        genres = this_movie['genres']
                        
                         #Update actor-genre count for each actor
                        for actor in this_movie['actors']:
                                actor_id, actor_name = actor
                                for genre in genres:
                                        if genre not in actor_genre_count[actor_name]:
                                                actor_genre_count[actor_name][genre] = 0
                                        actor_genre_count[actor_name][genre] += 1 
        
        #Convert actor-genre dict to df
        actor_genre_df = pd.DataFrame.from_dict(actor_genre_count, orient = 'index')
        
        #Coalculate cosine distance 
        cosine_distance = cosine_distances(actor_genre_df)
        query_idx = actor_genre_df.index.get_loc(query)
        cosine_distances_to_query = cosine_distance[query_idx]
        
        #create df for cosine distances
        cosine_distance_df = pd.DataFrame({ 'actor': actor_genre_df.index, 'cosine_distance': cosine_distances_to_query}).sort_values(by='cosine_distance')
        first_10_cosine = cosine_distance_df.head(11)[1:] 
       
        #calculate euclidean distance
        euclidean_dist = DistanceMetric.get_metric('euclidean')
        euclidean_distances_to_query = euclidean_dist.pairwise(actor_genre_df)[query_idx]
        
        #create df for euclidean distances
        euclidean_distance_df = pd.DataFrame({'actor': actor_genre_df.index, 'euclidean_distance': euclidean_distances_to_query}).sort_values(by='euclidean_distance')
        first_10_euclidean = euclidean_distance_df.head(11)[1:]
        
        #output to csv file
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/similar_actors_genre_{current_datetime}.csv"
        first_10_cosine.to_csv(output_path, index=False)