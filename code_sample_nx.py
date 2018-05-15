import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df_plot = pd.read_csv('filepath') #csv generated from separate program that uses beautifulsoup to read through online activity

#CREATE GRAPH AND CALCULATE CENTRALITIES / GENERATE LABELS FOR TOP ENGAGEMENT TARGETS
plt.figure(figsize = (10, 8))
G = nx.from_pandas_dataframe(df_plot, 'From', 'To', 'Order') #'Order' described type of connection (not visualized but used separately to inform engagement)
centrality = nx.degree_centrality(G)
df_cent = pd.DataFrame(list(centrality.items()), columns = ['Name', 'Centrality']).sort_values(by = 'Centrality', ascending = False)
hubs = df_cent['Name'].head(24).unique() #Get top 20 hubs, outside of 4 known centers of activity, which are known to have high centrality figures
centers = ['Primary A', 'Primary B', 'Primary C', 'Primary D']
labels = {}
pos = nx.spring_layout(G)
for i, node in enumerate(G.nodes()) : #Generate labels the graphic with numbers for hubs (to be printed later for number / hub identification) and full names for centers of activity
    if node in hubs :
        labels[node] = i
    if node in centers :
        labels[node] = node
nx.draw(G, pos = pos, with_labels = False, node_color = 'black', alpha = 0.25, node_size = 3, linewidths = 0.75)
nx.draw_networkx_labels(G, pos, labels, font_size = 8, font_color = 'red', font_weight = 'bold')
plt.show()

#PRINT LABELS CORRESPONDING TO GRAPH
for k, v in labels.items() : #Print the number and corresponding name for each hub for reference (minus the hubs we already have identified)
    if k in centers :
        continue
    else :
        print (v, '-', k)
