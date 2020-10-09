// Cypher import exmaples
CALL apoc.import.graphml("wn_full.graphml", {readLabels: true})

MATCH (n {type:"wordSense"})
SET n:WORDSENSE;

MATCH (n {type:"synset"})
SET n:SYNSET;

// Create direct wordsense connections
MATCH (w1:WORDSENSE)<-[:has_member]-(s:SYNSET)-[:has_member]->(w2:WORDSENSE)
WHERE id(w1) > id(w2)
MERGE (w1)-[:shared_synset]-(w2)

// 76403 Word-to-Word connections
// 779383 total paths
// Created 113696 relationships, completed after 2138 ms.

// Delete synsets to leave only new connections
MATCH (s:SYNSET)
DETACH DELETE s

// wordsense_to_wordsense graph export up to 3 hops away
CALL apoc.export.graphml.query('MATCH p=(n:WORDSENSE)-[*..3]-(m) WHERE n.lemma = "establishment"
RETURN p','orig_establishment_upto3.graphml',{})

// full db of shared synsets
CALL apoc.export.graphml.query('MATCH (w1:WORDSENSE)-[r:shared_synset]-(w2:WORDSENSE) RETURN w1, r, w2','wordsense_graph_full.graphml',{})

// all connectoins within 3 hops of "establishment" as the starting point
CALL apoc.export.graphml.query('MATCH (n)-[*..4]-(m) WHERE n.lemma CONTAINS "establishment" RETURN n,m','test_out.graphml',{})

// example Neo4j shortest paths query
MATCH p=allShortestPaths((n)-[*..10]-(m))
WHERE n.lemma = 'establishment' AND m.lemma = 'republic'
RETURN p