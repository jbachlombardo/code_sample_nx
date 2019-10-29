import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from network_fcns import get_commenters, get_likers, get_sharers, is_in, give_rank, survey_to_nx
pd.set_option('display.max_rows', None)

# Getting & Cleaning Data

source1_comms = get_commenters('source1_115Fsource4_comments.html', 'focal_point', 'Primary')
source1_survey_1 = survey_to_nx('Survey 8 -- for nx.csv')
source1_survey_2 = survey_to_nx('Survey 9 -- for nx.csv')
source1_eng = pd.read_csv('source1_engage_115Feb.csv')
source1 = pd.concat([source1_comms, source1_survey_1, source1_survey_2, source1_eng])

source2_likes = get_likers('RadioSouriaLi_likes.html', 'source2_Li', 'Like')
source2_comms = get_commenters('RadioSouriaLi_comments.html', 'source2_Li', 'Comment')
source2_shares = get_sharers('RadioSouriaLi_shares.html', 'source2_Li', 'Share')
source2 = pd.concat([source2_likes, source2_comms, source2_shares])

source3_likes = get_likers('source3_likes.html', 'source3', 'Like')
source3_comms = get_commenters('source3_comments.html', 'source3', 'Comment')
source3_shares = get_sharers('source3_shares.html', 'source3', 'Share')
source3 = pd.concat([source3_likes, source3_comms, source3_shares])

source1_comms = get_commenters('source1_comments_1831Dec.html', 'focal_point', 'Primary')
source1_survs = survey_to_nx('source1_responses_survey5.csv')
source1_eng = pd.read_csv('source1_engage_1831Dec.csv')

source4_comms = get_commenters('enabbaladi_comments_18Dec.html', 'source4', 'Comment')
source4_likes1 = get_likers('enabbaladi_likes_18Dec.html', 'source4', 'Like')
source4_likes2 = get_likers('enabbaladi_likes_18Dec_2.html', 'source4', 'Like')
source4_likes = pd.concat([source4_likes1, source4_likes2]).drop_duplicates('To', keep = 'first')
source4_shares = get_sharers('enabbaladi_shares_18Dec.html', 'source4', 'Share')
source5_likes = get_likers('newsyrian_likes_Dec.html', 'source5', 'Like')
source5_comms = get_commenters('newsyrian_comments_Dec.html', 'source5', 'Comment')
source5_shares = get_sharers('newsyrian_shares_Dec.html', 'source5', 'Share')
source6_likes = get_likers('aljumhuriya_likes_1118Dec.html', 'source6', 'Like')
source6_comms = get_commenters('aljumhuriya_comments_1118Dec.html', 'source6', 'Comment')
source6_shares = get_sharers('aljumhuriya_shares_1118Dec.html', 'source6', 'Share')
source7_comms = get_commenters('source7_comments.html', 'source7', 'Comment')

source8_likes = get_likers('source8_likes_1831Dec.html', 'source8', 'Like')
source8_comms = get_commenters('source8_comments_1831Dec.html', 'source8', 'Comment')
source8_shares = get_sharers('source8_shares_1831Dec.html', 'source8', 'Share')
source9_comms = get_commenters('source9_comments_31Dec.html', 'source9', 'Comment')
source9_shares = get_sharers('source9_shares_31Dec.html', 'source9', 'Share')

# Compiling DFs by community
source1 = pd.concat([source1_comms, source1_survs, source1_eng])
source4 = pd.concat([source4_comms, source4_likes, source4_shares])
source5 = pd.concat([source5_likes, source5_comms, source5_shares])
source6 = pd.concat([source6_likes, source6_comms, source6_shares])
source8 = pd.concat([source8_likes, source8_comms, source8_shares])
source9 = pd.concat([source9_comms, source9_shares])

#SYR2028 CENTRALITY
S = nx.from_pandas_dataframe(source1, 'From', 'To', 'Order')#['Order', 'Colors'])
source1_centrality = nx.degree_centrality(S)
source1_cent = pd.DataFrame(list(source1_centrality.items()), columns = ['Name', 'Centrality']).sort_values(by = 'Centrality', ascending = False)
source1_cent = source1_cent.rename(columns = {'Name': 'To'})
print (source1_cent.head(25))

Plotting DF
df_plot = pd.concat([source1, source2, source3])

#CREATE & IMPORT HOLDING CSV
df_plot.to_csv('df_plot_dated_210218.csv')
print ('Done!')
print ('plotting df is', len(df_plot), 'lines long')

# df_plot = pd.read_csv('df_plot_dated_210218.csv')

#Remove buggy entries
ords = df_plot['Order'].unique()
cols = list(range(len(ords)))
col_dict = dict(zip(ords, cols))
df_plot['Colors'] = df_plot['Order'].map(col_dict)
df_plot = df_plot.drop_duplicates(subset = ['From', 'To'])
isin = df_plot.loc[(df_plot['To'].isin(df_plot['From'])) & (df_plot['From'].isin(df_plot['To']))]
uni = isin['To'].unique()
rid = isin.loc[df_plot['From'].isin(uni)]
df_plot = pd.concat([df_plot, rid]).drop_duplicates(keep = False)

#Slice df_plot
df_plot = df_plot[(df_plot['From'] != 'Messenger') & (df_plot['From'] != 'source9') & (df_plot['From'] != 'source8')]

# Plot & Get Hubs
plt.figure(figsize = (10, 8))
G = nx.from_pandas_dataframe(df_plot, 'From', 'To', 'Order')#['Order', 'Colors'])
centrality = nx.degree_centrality(G)
df_cent = pd.DataFrame(list(centrality.items()), columns = ['Name', 'Centrality']).sort_values(by = 'Centrality', ascending = False)
hubs = df_cent['Name'].head(24).unique()
centers = ['focal_point', 'Messenger', 'source3', 'source2_Li']
labels = {}
pos = nx.spring_layout(G)
for i, node in enumerate(G.nodes()) :
    if node in hubs :
        labels[node] = i + 1
    if node in centers :
        labels[node] = node
labels_print = labels.copy()
nx.draw(G, pos = pos, with_labels = False, node_color = 'black', alpha = 0.25, node_size = 4, linewidths = 1)
nx.draw_networkx_labels(G, pos, labels, font_size = 8, font_color = 'red')
for center in centers :
    labels_print.pop(center)
for k, v in labels_print.items() :
    print (v, '-', k)
plt.title(" 1-15 source1 activity ")
plt.show()
print ('done')
df_cent = df_cent.rename(columns = {'Name': 'To'})

Finding targets
source1 = source1[(source1['From'] == 'focal_point') | (source1['From'] == 'Messenger')]

source1_rs = give_rank(source1, source2)
source1_rn = give_rank(source1, source3)

targets1 = df_cent.merge(source1_rs, on = 'To')
targets2 = df_cent.merge(source1_rn, on = 'To')
targets = pd.concat([targets1, targets2])
targets = targets[(targets['From_x'] == 'Messenger')].groupby('To').agg({'Centrality': 'mean', 'Value': 'sum', 'From_y': 'unique'})
targets.sort_values(by = 'Centrality', ascending = False).to_excel('targets_source1_21Feb.xlsx')
print ('Done')

source1_source2 = give_rank(source1, source2)
source1_source3 = give_rank(source1, source3)
source1_source4 = give_rank(source1, source4)
source1_source7 = give_rank(source1, source7)
source1_source8 = give_rank(source1source8)
source1_source9 = give_rank(source1, source9)

source1_targets = pd.concat([source1_source2, source1_source3])
print (source1_targets)

source1_targets.to_csv('targets_1831Dec.csv')
