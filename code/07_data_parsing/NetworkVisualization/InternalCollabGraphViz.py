
import sys,os,glob
sys.path.insert(0,"/usr/local/lib/python3.7/site-packages")
import pandas as pd
from graphviz import Graph
import networkx as nx
import numpy as np


def is_new(links,older_link_list):
    # check if links are in older link list
    # if true, then links are old
    # otherwise they are new
    l1=links[0]
    l2=links[1]
    l1l2_new=True
    # if self-loop, return
    if l1==l2:
        return l1l2_new
    
    # check if [l1,l2] exists in older link list
    for [old_l1,old_l2] in older_link_list:
        if (l1 == old_l1 or l1==old_l2) and (l2 == old_l1 or l2==old_l2):
            # link is old
            l1l2_new=False
            return l1l2_new
    # if link not found in older list, link is new
    return l1l2_new
        
def form_network(field,inst):
    df2012 = pd.read_csv('indiv_collab/cumul_indiv_collab_'+field.lower()+'_2012.csv',header=None)
    df2012.columns = ['node1','node2','inst1','inst2']
    
    df2012_inst = df2012.loc[(df2012['inst1']==inst)|(df2012['inst2']==inst),df2012.columns]
    df2012_links = df2012_inst.loc[:,['node1','node2']].values
    df2012_nodes = list(df2012_inst.loc[:,'node1'].values)+list(df2012_inst.loc[:,'node2'].values)
    
    df2017 = pd.read_csv('indiv_collab/cumul_indiv_collab_'+field.lower()+'_2017.csv',header=None)
    df2017.columns = ['node1','node2','inst1','inst2']
    df2017_inst = df2017.loc[(df2017['inst1']==inst)|(df2017['inst2']==inst),df2017.columns]
    df2017_links = df2017_inst.loc[:,['node1','node2']].values
    df2017_nodes = list(df2017_inst.loc[:,'node1'].values)+list(df2017_inst.loc[:,'node2'].values)

    G=nx.Graph()
    
    # record whether node is inside or outside institution
    # record age
    nodes2012_attr = {'node':[],'inst':[],'age':[]}
    for node in df2017_nodes:
        nodes2012_attr['node'].append(node)
        inst = list(df2017_inst.loc[df2017_inst['node1']==node,'inst1'])+list(df2017_inst.loc[df2017_inst['node2']==node,'inst2'])
        inst=inst[0]
        isnew=not (node in df2012_nodes)
        #nodes2012_attr['node'].append(node)
        #nodes2012_attr['inst'].append(inst)
        #nodes2012_attr['age'].append()
        G.add_node(node,institute=inst,new=int(isnew))
        
        

    
    for l1,l2 in df2017_links:
        # find age:
        age=is_new([l1,l2],df2012_links)
        G.add_edge(l1,l2)
        G[l1][l2]['new'] = int(age)
    for component in list(nx.connected_components(G)):
        if len(component)<=19:#12:
            for node in component:
                G.remove_node(node)
    print(list(G.degree))
    #print([G.degree(n) for n in G.neighbors(np.int64('2104514069'))])
    # we have node and link attributes we can exploit for graphviz
    return G

def display_network(G,inst_id,inst):
    g = Graph('G',filename='internal_network_'+inst+'_new_colors.gv',engine='fdp')
    g.attr(rankdir='LR',ratio='1')#,size='2,5')
    g.attr('node',shape='circle',fixedsize='true',width='0.2',color='black',style='filled')
    inst_nodes = []
    for node,attr_dict in G.nodes.data():
        #print(node)
        c='black'
        if attr_dict['new']==1:
            c = 'white'
        if attr_dict['institute']==inst_id:
            inst_nodes.append(node)
        elif attr_dict['institute']!=inst_id:
            c='plum'
        g.node(str(node),fillcolor=c,label='')
    #print(G.edges.data())
    for e1,e2,attr_dict in G.edges.data():
        
        if e1 in inst_nodes and e2 in inst_nodes:
            s=''
            c='forestgreen'#'darkgreen'
            if attr_dict['new']==1:
                c='forestgreen'
                s='dashed'
        else:
            c='orchid'
            s=''
            if attr_dict['new']==1:
                c='orchid'
                s='dashed'
        #l='4'
        
        #    l='1'
        #if e1 in inst_nodes and e2 in inst_nodes:
        g.edge(str(e1),str(e2),color=c,style=s,penwidth='3')
    
    g.view()

def main():
    
    institutions={'Stanford':np.int64('97018004')}#{'USC':np.int64('1174212'),'MIT':np.int64('63966007'),'Stanford':np.int64('97018004'),'Harvard':np.int64('136199984')}
    for field in ['Sociology']:
        for inst in institutions.keys():
            inst_id=institutions[inst]
            # color nodes in 2012 and edges in 2012 differently
            # i.e., denote which nodes are old and which are new
            # but use 2017 network to make graph
            G = form_network(field,inst_id)

            display_network(G,inst_id,inst)
            
        
if __name__ == "__main__":
    main()
        


    
