import os
import json
import pickle

import networkx as nx
import pandas as pd

import numpy as np

nodeList = pickle.load(open('nodeList.pkl','rb'))
edgeList = pickle.load(open('edgeList.pkl','rb'))

def condenseEdgeType(intype):
    if intype in ['has_member','~','~i','#p','%p','>']:
        return '+'
    elif intype in ['@','@i','#m','#s','%m','%s']:
        return '-'
    return np.nan

# By default, don't condense edge types, but switch to True if desired
'''
condense = False
print('total edges', len(edges))
if condense:
    edges['type'] = edges['type'].apply(condenseEdgeType)
    edges['weight'] = edges['type'].apply(lambda x: 1 if x=='+' else -1)
    edges = edges.dropna()
print('selected edge types', len(edges))
'''
# Build networkx graph from nodeList and edgeList
G = nx.Graph()

print('Adding nodes to graph')
for i, node in enumerate(nodeList):
    if i % 100000 == 0:
        print(i)
    
    toPop = []
    for key in node.keys():
        if node[key] == None:
            toPop.append(key)
    for key in toPop:
        node.pop(key)
    node['label'] = ':' + node['type']
    
    G.add_node(node['name'])
    for key in node.keys():
        G.nodes[node['name']][key] = node[key]

print('Adding edges to graph')
for i, edge in enumerate(edgeList):
    if i % 100000 == 0:
        print(i)
    #print(edge)
    G.add_edge(edge['source'],edge['target'])
    G.edges[edge['source'],edge['target']]['label'] = edge['type']
    if 'weight' in edge.keys():
        G.edges[edge['source'],edge['target']]['weight'] = edge['weight']
    else:
        G.edges[edge['source'],edge['target']]['weight'] = 1.0
        #print(e)
        #print(edge)
        #break
        
nx.write_graphml(G,'./wn_full.graphml')