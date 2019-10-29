# NetworkX code sample

(Full workflow contained in network_graphing.py, with helper functions in network_fcns.py.)

This code sample demonstrates how network analysis was used to assess and visualize digital networks. The goal of our analysis was to identify the most important nodes, which were to be targeted for further engagement given their centrality to the network.

The inputs were generated from survey activity (gathered via a Messenger bot, plus a Zapier webhook / Google Sheets integration) and online activity around owned platforms (parsed using beautifulsoup). These were then merged into a single dataframe (referenced in the fifth line of the code sample) structured to show information flow from node to node. This was then used to visualize the network and calculate the degree centralities, which were the basis for our next steps.

This created the following image, which we used for presentations.

(Inputs anonymized for this sample.)

![nximage](https://jbachlombardo.files.wordpress.com/2018/03/network-activity.png)
