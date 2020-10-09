import os
import json
import pickle

import networkx as nx
import numpy as np
import pandas as pd


fnames = os.listdir('./data/wordnet-3.3/')
dataFiles = [fname for fname in fnames if fname[:4] == 'data']

print('found datafiles', dataFiles)

data = []

# One file for every PoS
for dataFile in dataFiles:
    
    # read the file in line by line
    with open('./data/wordnet-3.3/'+dataFile,'r') as f:
        lines = f.readlines()
    
    # first several lines are copyright disclaimer
    for line in lines[29:]:
        # cull newline char and skip empty lines
        line = line.replace('\n','')
        if len(line) == 0:
            continue
        # each line has two parts
        fields, example = line.split('|')
        # spaces delimit within the fields
        fields = fields.split(' ')
        #print(fields)
        synset = {}
        
        # Populate synset fields
        synset['offset'] = fields[0]
        synset['lexFileNum'] = int(fields[1])
        synset['type'] = fields[2]
        # nWords is stored as a hex int, so convert that
        synset['nWords'] = int(fields[3], 16)
        # There are two fields per word for the number of words 
        # following the first 4 (above) fields
        wordData = fields[4:4+synset['nWords']*2]
        
        # Populate the word data into a new list of word info
        words = []
        #print(len(wordData))
        for i in range(0, synset['nWords']):
            words.append({'lemma':wordData[2*i],'sense':wordData[2*i+1]})
        synset['words'] = words
        
        # There will be a pointer for each word
        synset['nPointers'] = int(fields[4+synset['nWords']*2])
        # Easier to pull from a new list of just relevant fields
        pointerData = fields[4+synset['nWords']*2+1:]
        pointers = []
        
        # Add the four attrs using index offsets
        for i in range(0, synset['nPointers']):
            thisPointer = {'symbol':pointerData[4*i], 'offset':pointerData[4*i+1],
                             'pos':pointerData[4*i+2], 'source/target':pointerData[4*i+3]}
            #print(thisPointer)
            pointers.append(thisPointer)
        
        # Set the pointers and append the synset to the data
        synset['pointers'] = pointers
        data.append(synset)
    
    print(dataFile,'added; data is now', len(data), 'rows')

# Iterate through the data and begin network buildout
edgeList = []
nodeList = []

wordSenseLookup = {}
wordSensePointerList = []

for synset in data:
    # Add synset to graph
    nodeList.append({'name': synset['offset'], 'type':'synset',
                     'pos':synset['type'], 'nwords':synset['nWords']})
    
    # For looking up words at a certain position later: synset offset-->words
    wordSenseLookup[synset['offset']] = synset['words']
    
    # Add both the sense and lemma as nodes and connect them to synset and each other
    for word in synset['words']:
        wordSense = word['lemma']+'_'+word['sense']
        nodeList.append({'name': wordSense,
                         'type':'wordSense', 'lemma': word['lemma'], 'sense': word['sense']})
        # Removing lemma rels for this run
        #nodeList.append({'name': word['lemma'], 'type': 'lemma'})
        #edgeList.append({'source':word['lemma'], 'type':'has_sense', 'target':wordSense})
        
        edgeList.append({'source':synset['offset'], 'type':'has_member', 'target':wordSense})
    
    # Connect the pointer info for wordsense to wordsense connection
    for pointer in synset['pointers']:
        # we'll worry about normalizing the directions later
        if pointer['source/target'] == '0000':
            #print(pointer)
            edgeList.append({'source': synset['offset'], 'type': pointer['symbol'],
                             'target': pointer['offset']})
        else:
            # append any sense-to-sense pointers
            wordSensePointerList.append({'source':synset['offset'], 'pointer':pointer})
            
# this must be run after all senses are seen for an error not to be thrown on target lookup
errorCount = 0
suppressErrors = True
for entry in wordSensePointerList:
    sourceWords = wordSenseLookup[entry['source']]
    #print(sourceWords)
    try:
        targetWords = wordSenseLookup[entry['pointer']['offset']]
    except KeyError as e:
        print('target word not found')
        continue
    #print(targetWords)
    
    # set vars to keep track of synset offsets
    sourceOffset = entry['source']
    targetOffset = entry['pointer']['offset']
    #print(sourceOffset, targetOffset)
    
    # the indices within the synsets (these are 1-indexed, our lists 0)
    sourceWordIndex = int(entry['pointer']['source/target'][0:2],16)-1
    targetWordIndex = int(entry['pointer']['source/target'][-2:],16)-1

    try:
        # create the senses as lemma + sense_number
        sourceSense = sourceWords[sourceWordIndex]['lemma']+'_'+sourceWords[sourceWordIndex]['sense']
        targetSense = targetWords[targetWordIndex]['lemma']+'_'+targetWords[targetWordIndex]['sense']

        # append the new relationship
        edgeList.append({'source':sourceSense, 'type':entry['pointer']['symbol'], 'target':targetSense})
    except IndexError as e:
        errorCount += 1
        if not suppressErrors:
            print(sourceWordIndex, targetWordIndex)
            print(sourceWords, '\n', targetWords)
print('number of invalid connections in source data:',errorCount)

len(edgeList), len(nodeList)


# Output data to csv formats
print('writing out parsed results in pickle, csv, and json format')

pickle.dump(nodeList, open('nodeList.pkl','wb'))
pickle.dump(edgeList, open('edgeList.pkl','wb'))

nodeDF = pd.DataFrame(nodeList)
edgeDF = pd.DataFrame(edgeList)

print(edgeDF['type'].value_counts())

nodeDF.to_csv('edgeList.csv',index=False)
edgeDF.to_csv('nodeList.csv',index=False)
nodeDF.to_json('nodes.json', orient='records')
edgeDF.to_json('edges.json',orient='records')