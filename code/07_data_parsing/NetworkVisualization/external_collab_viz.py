# need this to import networkx
import sys,os
sys.path.insert(0,"/usr/local/lib/python3.7/site-packages")
import matplotlib.cm as cm
import pandas as pd
import numpy as np
import networkx as nx
import graphviz as gv
from graphviz import Graph
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from glob import glob
import random

verbose=True

def find_data_files(field):
    edgefiles2017 = glob('external_collab/'+field.lower()+'_inst_cumul_collab_2017/*.csv')
    random.shuffle(edgefiles2017)
    nodefiles2017 = glob('InstituteCollaborationData/'+field+'/institution_description/*.csv')
    random.shuffle(nodefiles2017)
    return [nodefiles2017,edgefiles2017]

def find_size(df,year):
    size = df.loc[df['year']<=year,'cumul_size']
    if len(size) > 0:
        s = max(size)
    else:
        s = 0
    return s


def get_node_attributes(nodefiles):
    size_dict = {}
    growth_dict = {}
    node_names = []
    for file in nodefiles:
        inst_id = file.split('/')[-1].split('.')[0]
        node_names.append(inst_id)
        df=pd.read_csv(file)
        size2012 = find_size(df,2012)
        size2017 = find_size(df,2017)
        size_dict[inst_id] = size2017
        growth = size2017-size2012
        growth_dict[inst_id] = growth
    return [size_dict,growth_dict,node_names]

def create_graph_nodes(nodefiles):
    G=nx.Graph()
    size_dict,growth_dict,node_names = get_node_attributes(nodefiles)
    G.add_nodes_from(node_names)
    #print(size_dict)
    nx.set_node_attributes(G, size_dict, 'size')
    nx.set_node_attributes(G, growth_dict, 'growth')
    return G

def append_edges(edges,df,edgefile2012,inst_id,threshold):
    edgefile2012_exists = os.path.exists(edgefile2012)
    if edgefile2012_exists:
        df2012 = pd.read_csv(edgefile2012,header=None)
    for i,row in df.iterrows():
        old_edge = 0
        if edgefile2012_exists:
            if row[0] in df2012.iloc[:,0].values:
                old_edge = df2012.loc[df2012[0]==row[0],1].values[0]
        w = row[1]
        if w > threshold:
            edges.append((inst_id,str(row[0]),{'weight':w,'growth':w-old_edge}))


def get_edges(edgefiles,threshold):
    edges = []
    for file in edgefiles:
        inst_id = file.split("_")[8]
        field = file.split("_")[-2]
        edgefile2012 = 'external_collab/sociology_inst_cumul_collab_2012/cumul_inst_collab_'+inst_id+'_'+field+'_2012.csv';
        df2017 = pd.read_csv(file,header=None)
        append_edges(edges,df2017,edgefile2012,inst_id,threshold)
        
    return edges

def get_graph_attributes(G):
    node_sizes = nx.get_node_attributes(G,'size');
    
    node_size_growth = nx.get_node_attributes(G,'growth');
    edge_sizes = nx.get_edge_attributes(G,'weight')
    edge_size_growth = nx.get_edge_attributes(G,'growth')
    return [node_sizes,node_size_growth,edge_sizes,edge_size_growth]

def find_node_color(val):
    c = colors.to_hex(cm.plasma(1-np.log10(val)/3.5))
    return c
def find_edge_color(val):
    c = colors.to_hex(cm.plasma(1-np.log10(val)/2))
    return c


def strHex(num):
	return ("0x%0.2X" % int(num)).split('x')[1]
def find_alpha(fl):
    return strHex(min([1,fl])*256)
def change_node_size(G,g):
    node_sizes,node_size_growth,edge_sizes,edge_size_growth = get_graph_attributes(G)
    for node in G.nodes:
        if node in node_sizes.keys():
            s = node_sizes[node]
            growth = node_size_growth[node]
        else:
            print(node+" missing")
            s=1
            growth=0
        lab = ""
        if node == "136199984":#Harvard
            lab = 'Harvard'
        if node == "97018004":#Stanford
            lab='Stanford'
        if node == "63966007":#MIT
            lab='MIT'
        if node == "97018004":#USC
            lab='USC'
        if node == "20231570": #peking university
            lab = 'Peking'
        if node == "40120149": #Oxford
            lab = 'Oxford'
        if lab!="":
            print(lab)

        g.node(node,width=str(max([0.01,np.log10(s+0.01)/12])),height=str(max([0.01,np.log10(s+0.01)/12])),style='filled',fillcolor=find_node_color(growth+0.1),label=lab,fontcolor='white')
def change_edge_size(G,g,thresh):
    node_sizes,node_size_growth,edge_sizes,edge_size_growth = get_graph_attributes(G)
    # only show significant edges
    
    for edge in G.edges:
        s = edge_sizes[edge]
        if s > thresh:
            growth = edge_size_growth[edge]
            w = str(np.log10(s)*5)
            #print(w)
            color = find_edge_color(growth+0.1)
            
            g.edge(edge[0],edge[1],penwidth=w,weight=w,color=color+'5f',minlen='10')#+find_alpha(growth))


def visualize_graph(G,file,thresh):
    
    g = Graph('G', filename=file, engine='fdp')
    g.attr('node', shape='circle', fixedsize='true', width='0.2',rankdir='LR')
    change_node_size(G,g)
    if verbose:
        print("nodes visualized")
    change_edge_size(G,g,thresh)
    if verbose:
        print("edges visualized")
    #plt.colorbar()

    g.view()

def main():
    
    field = 'Sociology';
    threshold = 10;
    nodefiles2017,edgefiles2017=find_data_files(field)
    
    G = create_graph_nodes(nodefiles2017)
    if verbose:
        print("nodes created")
    edges = get_edges(edgefiles2017,threshold)

    G.add_edges_from(edges)

    isolated_nodes = [n for n,k in G.degree if k<= 0]
    G.remove_nodes_from(isolated_nodes)

    if verbose:
        print("edges created")
    file = 'external_collab_'+field+'_threshold=10_fdp_plasma_LR_transparent_thicker-edges_labeled_nodecolors.gv'
    visualize_graph(G,file,threshold)
    if verbose:
        print("graph created: {}".format(file))


if __name__ == "__main__":
    main()

