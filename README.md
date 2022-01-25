# Reproducing Heterogenous Scaling Laws for Research Institutions
## Code for preparation and analysis of Microsoft Academic Graph (vintage 2018)

### All code is for Python 3

Data pre-processing pipeline (1-6 below) developed by Zihao He ca. 2018-2019. Data analysis (7 below) and simulations developed by Keith Burghardt ca. 2018-2021. Discussions with some referees suggests that this pipeline may need to be amended for later versions of MAG. Any updates to this pipeline will be gladly accepted, and encouraged.

Data analysis requires the following libraries:
* pandas
* numpy
* graphviz (for network visualization in 07_data_parsing)
* statsmodels
* pickle
* networkx
* requests
* matplotlib


Simulations require the following libraries:
* pandas
* numpy
* scipy
* pickle

Please run data pipeline in the following order:

1. 01_mag_data_preprocessing
    *  These files collect data from MAG
    *  Run in order: 01_year_papernum.py, 02_paper_downloading.py
2. 02_paper_modeling
    *  Making sure papers are valid (contains dates, author IDs, affiliations, etc.,) and other data cleaning
    *  Run in order: 01_paper_cleaning.py, 02_paper_references.py, 03_citation_network.py, 04_paper_construction.py
3. 03_author_modeling
    *  Find when authors first published
4. 04_institution_modeling
    *  Reconstruct affiliations/collaborations
    *  Run in order: 01_affiliation_papers.py, 02_affiliation_construction.py, 03_output_affiliation.py, 04_output_affiliation_author.py
5. 05_dataset_description
    *  Collect together affiliations, institution impact, etc., into one file
    *  Also collect both yearly and cumulative data (yearly results are shown in the SI)
    *  Run in order: 01_authorId_sequence&affId_sequence.py, 02_author_institution_sequence.py
6. 06_data_sequences
    *  This reconstructs sequences of affiliations of each researcher over time
    *  This is how we can reconstruct Zipf's and Heaps' laws for the datasets
    *  Run in order: 01_authorId_sequence&affId_sequence.py, 02_author_institution_sequence.py
7. 07_data_parsing
    *  This reconstructs data used in figures
    *  Graph visualizations in Fig. 1 can be reconstructed with files in the *NetworkVisualization* folder
    *  Data for Fig. 3 can be reconstructed with files in *ScalingLaws* folder
    *  Data statistics over time, seen in Fig. S1 of Supplementary Note 1 can be reconstructed with files in the *TimeSeries* folder
    *  Actual figures were made in Mathematica, but any figure-maker, like Python's matplotlib, will do. Furthermore, figures are combined with OmniGraffle, but again anyone's favorite software, such as PowerPoint, can be used to combine figures in Fig. 1 or make Fig. 3 schematic.

**entities** and **utils** are folders required for data pipeline

Simulations can be run via Simulation.py, where all fitting parameters are listed inside this file.
