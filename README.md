# WAFFLE
## A Graph for WordNet Applied to FreeForm Linguistic Exploration

<img src="./figures/figure_1.png" alt="Figure 1 from the WAFFLE paper" title="Figure 1 from the WAFFLE paper" width="800" height="400"/>

## Introduction
WAFFLE is a software research project that builds on the [WordNet](https://wordnet.princeton.edu/) lexical database by restructuring and exploring the database into a graph structure. In addition to the Python code that performs this transformations and outputs the results in accessible interchange formats (.csv, .graphml), we make available [openCypher](http://www.opencypher.org/) code for loading and transforming the WAFFLE graph as well as figures featured in the [WAFFLE paper and presentation](thomsonreuters.com) featured at the *2nd Workshop for Natural Language Processing Open Source Software* ([NLP-OSS 2020](https://nlposs.github.io/2020/index.html))

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Homemade_waffle_closeup.jpg/800px-Homemade_waffle_closeup.jpg" alt="waffle" title="photo of a real-world waffle" width="400" height="300"/>

<span style="font-size:0.75em"><a href="https://commons.wikimedia.org/wiki/File:Homemade_waffle_closeup.jpg">waffle photo credit</a></span>

## Code Structure
### Python
The WAFFLE Python code is split into two .py files designed to be run in sequence:
1. `parse_wn.py`: WAFFLE's first section parses and processes the native structure of the WordNet data (downloaded separately) and outputs an edge list and node list in `.csv` format as well as Python pickle (`.pkl`) format for use by the second half of WAFFLE
2. `build_waffle.py`: taking the raw graph structure from part 1, build_waffle.py uses the networkx package to assemble a wordsense- and synset-complete graph, exporting it in `.graphml` format for use in desktop network analysis software like Cytoscape and Gephi.

### Cypher
In addition to the WAFFLE graph creation code, we provide `import.cypher`, a Cypher-based collection of queries and function calls that were used during the analysis and preparation of the WAFFLE paper.

Note: While the syntax is in the OpenCypher format, certain function calls such as those to [APOC](https://neo4j.com/labs/apoc/) are specific to the [Neo4j](https://neo4j.com/) implementation this was tested with. When using these queries on other platforms, some modification will be necessary.

## Installation
### Python environment
WAFFLE requires the following non-standard Python libraries:
* numpy
* pandas
* networkx

These packages can be installed in a number of ways:
* The [Anaconda Python](https://www.anaconda.com/products/individual) distribution includes these packages and many others by default in their distribution. Users looking to get working with WAFFLE with as little configuration as possible should consider installing and using the Anaconda distribution
* Users of the Conda package manager who prefer not to install all the packages in Anaconda may use the provided environment.yml file as follows to create a new environment ready to run WAFFLE. The package versions in the environment.yml file have been tested for compatibility with WAFFLE
```bash
conda create --name waffle
activate waffle # conda activate waffle (if on Windows)
conda env create -f environment.yml
```
* Alternatively, users can create a new pip environment and install compatible versions of the packages without the use of Conda

###  WordNet data
parse_wn.py expects the WordNet data to be in the `./data/wordnet-3.3/` directory. WAFFLE is built to use the WordNet data as it's presented in the *wn* package by [NLTK](https://www.nltk.org/), available on GitHub at in the [project repository](https://github.com/nltk/wordnet/tree/master/wn/data/wordnet-3.3) under the Apache 2.0 license.

We have decided not to include a copy of the data with the WAFFLE repository at this time and instead ask users to please download from the NLTK *wn* repository.

## Figures
In addition to the WAFFLE code, we provide the two major figures featured in the WAFFLE publication on this repository freely for exploration and learning. Each figure is provided both as a `.png` image file and also the `.gephi` session files used to explore the networks and create the figures.

## Licenses

The WAFFLE code (Python and Cypher) are released under the [MIT License](https://opensource.org/licenses/MIT). Accompanying figures in `.png` and `.gephi` format are released under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) license. 
