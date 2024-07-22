
def GP2GraphToGP2StringDT_rule_precursor(GP2Graph,preserved_nodes_list = None):
    '''
    Produce one side of a GP2 rule from a GP2 graph representation of an Essence AST
    '''
    #random.shuffle(GP2Graph.nodes) #TODO seed with parameter
    ID_shift = len(GP2Graph.nodes)
    ID_shift_e = len(GP2Graph.edges)
    GP2String_DT = ""
    GP2String_DT += "[\n"
    info_edges_DT = ""
    for i,node in enumerate(GP2Graph.nodes):
        nodeid = int(node[0])
        if preserved_nodes_list == None or nodeid in preserved_nodes_list:
            GP2String_DT += f'(n{nodeid},\"{node[1]}")\n'
            GP2String_DT += f'(n{nodeid+ID_shift},\"{node[2]}\")\n'
            info_edges_DT+= f'(e{i+ID_shift_e*2},n{nodeid},n{nodeid+ID_shift}, \"info\")\n'
    GP2String_DT += "| \n"
    for edge in GP2Graph.edges:
        if preserved_nodes_list == None or (int(edge[1]) in preserved_nodes_list and int(edge[2]) in preserved_nodes_list):
            GP2String_DT += f'(e{edge[0]},n{edge[1]},n{edge[2]},{edge[3]})\n'
            GP2String_DT += f'(e{int(edge[0])+ID_shift_e},n{int(edge[1])+ID_shift},n{int(edge[2])+ID_shift},{edge[3]})\n'

    GP2String_DT += info_edges_DT
    GP2String_DT += "]"
    return GP2String_DT   

def GP2GraphToGP2StringB_rule_precursor(GP2Graph,preserved_nodes_list = None):
    '''
    Produce a GP2 representation of the graph in string format.
    '''
    #random.shuffle(GP2Graph.nodes) #TODO seed with parameter
    ID_shift = len(GP2Graph.nodes)
    ID_shift_e = len(GP2Graph.edges)
    GP2String_B = ""
    GP2String_B += "[\n"
    info_edges_B = ""
    for i,node in enumerate(GP2Graph.nodes):
        if type(node[0]) == str:
            print(node[0])
        nodeid = int(node[0])
        if preserved_nodes_list == None or nodeid in preserved_nodes_list:
            GP2String_B += f'(n{nodeid},\"{node[1]}")\n'
            GP2String_B += f'(n{nodeid+ID_shift},\"{node[2]}\")\n'
            info_edges_B+= f'(e{i+ID_shift_e*2},n{nodeid},n{nodeid+ID_shift}, 0)\n'
    GP2String_B += "| \n"
    for edge in GP2Graph.edges:
        if preserved_nodes_list == None or (int(edge[1]) in preserved_nodes_list and int(edge[2]) in preserved_nodes_list):
            GP2String_B += f'(e{edge[0]},n{edge[1]},n{edge[2]},{edge[3]})\n'
        #GP2String_B += f'({int(edge[0])+ID_shift_e},{int(edge[1])+ID_shift},{int(edge[2])+ID_shift},{edge[3]})\n'

    GP2String_B += info_edges_B
    GP2String_B += "]"
    return GP2String_B   