from treelib import Node, Tree
import xml.etree.ElementTree as ET
import re
import os

#
#Sample Annotation:
#
#
# What is the way things are?
# >###Q_1###
# >>###Answer_1’###
# >>###Question_2###
# >>>###Answer_2’###
# >>>###Answer_2’’###
# >>###Question_3###
# >>>###Answer_3###
# >>>###Question_4###
# >>>>###Answer_4###
# >>###Answer_1’’###
#


def createTreeFromFile(filename):
    '''
    create tree object from an annotation file

    Args:
        filename (str): path of the file that should be converted to a tree.

    Returns:
        tree: tree object from the treelib library
    '''
    tree = Tree()
    with open (filename, "r") as myfile:
        data=myfile.readlines()
    level_dict = dict()
    node_no=0
    tree.create_node(_getText(data[0]), node_no)
    level_dict[0] = node_no
    for node in data[1:]:
        node_no = node_no+1
        level = _getLevel(node)
        text = _getText(node)

        tree.create_node(text,node_no,parent=level_dict[level-1])
        level_dict[level] = node_no
    
    return tree



def _getText(string):
    '''
    get the text of an assertion or question from a line in the annotated file

    Args:
        string (str): line in the annotated file (e.g. >>Is this a QUD?)

    Returns:
        str: question or assertion text
    '''
    p = re.compile(">*(.*)\n")
    return p.match(string).group(1)



def _getLevel(string):
    '''
    get the level of an assertion or question from a line in the annotated file

    Args:
        string (str): line in the annotated file (e.g. >>Is this a QUD?)

    Returns:
        str: question or assertion level (in case of the example 2)
    '''
    p = re.compile(">*")
    return p.match(string).span()[1]-p.match(string).span()[0]



def checkLeaves(inputTextFilename, qudTree):
    '''
    Test if the leaf nodes actually represent the given text

    Args:
        inputTextFilename (str): path to the file with the segmented text (one segment per line)
        qudTree (Tree Obj): QUD-tree

    Returns:
        bool: true if all leaves are correct else false
    '''
    with open(inputTextFilename) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    leaf_fit = [leaf.tag == text for leaf, text in zip(qudTree.leaves(), content)]
    return all(leaf_fit)



def checkBigQuestion(qudTree):
    '''
    Check if the big question at the root of the tree is \"What is the way things are?\" 

    Args:
        qudTree (Tree Obj): QUD-tree

    Returns:
        bool: true if root node is correct else false
    '''
    return qudTree[0].tag == "What is the way things are?"



def tree2XML(tree, filename):
    '''
    Convert QUD-tree to XML and write to file

    Args:
        tree (Tree Obj): QUD-tree
        filename (str): filepath the xml should be written to

    Returns:
        bool: true if root node is correct else false
    '''
    node_dict = {}
    for node_id in tree.nodes:
        attrDict = {}
        if tree.get_node(node_id).is_leaf():
            attrDict["surface"] = tree.get_node(node_id).tag
            attrDict["category"] = ""
        else:
            attrDict["surface"] = ""
            attrDict["category"] = tree.get_node(node_id).tag

        if tree.parent(node_id) == None:
            node_dict[node_id] = ET.Element("node", surface=attrDict["surface"], category=attrDict["category"])  
        else:
            node_dict[node_id] = ET.SubElement(node_dict[tree.parent(node_id).identifier], 'node', surface=attrDict["surface"], category=attrDict["category"])
        
    XMLtree = ET.ElementTree(node_dict[0])
    XMLtree.write(filename + '.xml')
    return XMLtree