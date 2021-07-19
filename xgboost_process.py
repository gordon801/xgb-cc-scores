import pandas as pd
import re
import sys
import os

# define Node class
class Node:
    # value = leaf value, compFactor = factor used for comparison (e.g. sub_grade_n)
    # compValue = value used for comparison, leftNode = left attached node, rightNode = right attached Node
    def __init__(self, leafValue = None, compFactor = None, compValue = None, leftNode = None, rightNode = None):
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.leafValue = leafValue
        self.compFactor = compFactor
        self.compValue = compValue

    # defining class getters and setters
    def setLeft(self, node):
        self.leftNode = node

    def setRight(self, node):
        self.rightNode = node

    def getLeftNode(self):
        return self.leftNode

    def getRightNode(self):
        return self.rightNode

    def getLeafValue(self):
        return self.leafValue

    def getCompFactor(self):
        return self.compFactor

    def getCompValue(self):
        return self.compValue

# define Tree class
class Tree:
    def __init__(self, root):
        self.root = root

    # traversal method (go to right node if compValue < value of data point for a particular compFactor, else right)
    def traversal(self, data_point):
        currentNode = self.root
        while currentNode.getLeafValue() == None:
            compFactor = currentNode.getCompFactor()
            compValue = currentNode.getCompValue()
            if compValue < data_point[compFactor]:
                currentNode = currentNode.getRightNode()
            else:
                currentNode = currentNode.getLeftNode()

        # return leaf value (i.e. bottom node of tree)
        return currentNode.getLeafValue()


# import xgb trees
def import_trees(xgb_trees):
    # split trees by the delimiter "booster", then delete the empty 1st element in list
    xgb_trees = xgb_trees.read()
    xgb_trees_list = xgb_trees.split('booster')
    xgb_trees_list.remove('')

    # split each tree into nodes
    xgb_trees_split = []
    for i in xgb_trees_list:
        node_split = i.splitlines()
        del node_split[0]
        xgb_trees_split.append(node_split)

    return xgb_trees_split

# generate root nodes from list of nodes
def generate_nodes(xgb_trees):
    xgb_trees_split = import_trees(xgb_trees)

    xgb_root_nodes = []
    for tree in xgb_trees_split:
        node_dict = {}
        for node in tree:
            # if leaf node, extract leaf value and node number, strip everything else
            # append to a dictionary of key [node number]
            # of information in order [Node, leftNode_number, rightNode_number]
            if 'leaf' in node:
                leaf_node_num = int(re.sub(r'\s+', '', node.split(':')[0]))
                leaf_value = float(node.split('leaf=')[1].split(',')[0])
                node_dict[leaf_node_num] = [Node(leaf_value), None, None]
                node_dict

            # else (non-leaf node need to get compFactors and compValues and left/right node numbers)
            # append to a dictionary of key [node number]
            # of information in order [Node, leftNode_number, rightNode_number]
            else:
                node_num = int(re.sub(r'\s+', '', node.split(':')[0]))
                node_compFactor = node.split('<')[0].split('[')[1]
                node_compValue = float(node.split('<')[1].split(']')[0])
                leftNode_number = int(node.split('yes=')[1].split(',')[0])
                rightNode_number = int(node.split('no=')[1].split(',')[0])
                node_dict[node_num] = [Node(None, node_compFactor, node_compValue), leftNode_number, rightNode_number]

        # link nodes based on leftNode_number and rightNode_number if non-leaf node (leaf nodes have no attached nodes)
        for key in node_dict:
            curr_node = node_dict[key][0]
            curr_node_leafValue = curr_node.getLeafValue()
            if curr_node_leafValue is None:
                leftNode_index = node_dict[key][1]
                rightNode_index = node_dict[key][2]
                node_dict[key][0].setLeft(node_dict[leftNode_index][0])
                node_dict[key][0].setRight(node_dict[rightNode_index][0])

        # append to list of root nodes (representing individual trees)
        xgb_root_nodes.append(node_dict[0][0])

    return xgb_root_nodes


# create data points for dataset
# data = dataframe format
def data_preparation(data):
    dataset = []
    for i in range(len(data)):
        data_point = data.iloc[i]
        dataset.append(data_point)
    return dataset


# generate trees from roots, and for each data point in dataset, traverse all trees using traversal function
def traverse_trees(xgb_trees, data):
    dataset = data_preparation(data)
    xgb_root_nodes = generate_nodes(xgb_trees)
    tree_list = []
    # create Trees from roots
    for root in xgb_root_nodes:
        tree_list.append(Tree(root))

    # track scores for each data point
    score_list = []
    for data_point in dataset:
        score = 0
        # for each datapoint, traverse each tree and sum score for each tree
        for tree in tree_list:
            curr_score = tree.traversal(data_point)
            score += curr_score
        score_list.append(score)
    return score_list


# import data
xgb_data = open(os.path.join(sys.path[2], 'xgb_tree_1000.txt'), "r")
cc_data = pd.read_csv(os.path.join(sys.path[2], 'creditcard_3001.csv'), low_memory=False)

# run function
score_list = traverse_trees(xgb_data, cc_data)

# print for exported file
for i in score_list:
    print(i)

