'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime
import json

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'


with open() as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
        # add the actor to the graph 
            g.add_node(actor_id, name = actor_name)   
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
        i = 0 #counter
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                # Get the current weight, if it exists
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                # Add an edge for these actors
                    g.add_edge(left_actor_id, right_actor_id, weight = 1)
                
                
            i += 1 


# Print the info below
print("Nodes:", len(g.nodes))
degree_centrality = nx.degree_centrality(g)
betweenness_centrality = nx.betweenness_centrality(g)
closeness_centrality = nx.closeness_centrality(g)

degree_df = pd.DataFrame(degree_centrality.items(), columns=['actor_id', 'degree_centrality'])
betweenness_df = pd.DataFrame(betweenness_centrality.items(), columns=['actor_id', 'betweenness_centrality'])
closeness_df = pd.DataFrame(closeness_centrality.items(), columns=['actor_id', 'closeness_centrality'])

centrality_df = degree_df.merge(betweenness_df, on='actor_id').merge(closeness_df, on='actor_id')

actor_names = nx.get_node_attributes(g, 'name')
centrality_df['actor_name'] = centrality_df['actor_id'].map(actor_names)

#Print the 10 the most central nodes
top_10_central = centrality_df.nlargest(10, 'degree_centrality')
print("Top 10 most central nodes:")
print(top_10_central)

# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"data/network_centrality_{current_datetime}.csv"
centrality_df.to_csv(output_path, index=False)

