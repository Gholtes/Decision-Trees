import graphviz as gv
import math
import pandas as pd
#init graphvis
g = gv.Digraph(format='svg')
node_names = ["yes"]

def import_golf(filename):
    data = pd.read_csv(filename)
    Y = data["Y"].tolist()
    X_dict = {}
    #interate through column names
    for column_name in list(data):
        if column_name != "Y":
            X_dict[column_name] = data[column_name].tolist()
    return Y, X_dict
#graphvis functions
def node(decision, color = "black"):
    if not (decision in node_names):
        node_names.append(decision)
        g.node(decision, color=color)
        return decision
    else:
        decision += " "
        return node(decision, color = color)
def edge(parent, child, branch = ""):
    g.edge(parent, child, branch)
def save(name):
  filename = g.render(filename=name)

def E(x,y):
    '''helper function to tidy Entropy'''
    tot_count = float(x+y)
    x = float(x) / tot_count
    y = float(y) / tot_count
    if x == 0 or y == 0:
        return 0
    else:
        return-x*math.log(x,2)-y*math.log(y,2)
def Entropy(Y, X = None):
    '''Compute entropy'''
    if X == None:
        Y_options = list(set(Y))
        count = [0 for _ in range(len(Y_options))]
        tot_count = len(Y)

        for i in range(len(Y)):
            count[Y_options.index(Y[i])] += 1

        entrop = 0
        for option_index in range(len(Y_options)):
            entrop += - (float(count[option_index]) / float(tot_count)) * math.log((float(count[option_index]) / float(tot_count)), 2)
        return entrop
    else:
        Y_options = list(set(Y))
        X_options = list(set(X))
        count = [[0 for _ in range(len(Y_options))] for _ in range(len(X_options))]
        tot_count = float(len(Y))

        for i in range(len(Y)):
            count[X_options.index(X[i])][Y_options.index(Y[i])] += 1

        entrop = 0
        for x in range(len(X_options)):
            entrop += (float(sum(count[x]))/tot_count)*E(count[x][0], count[x][1])

        return entrop

def InfoGain(Y, X):
    '''Y = the dependant variable, X = the dependnat variable being evaluated'''
    return Entropy(Y) - Entropy(Y, X)

def decide(Y, X_dict, previous_node):
    #Calc info gain for each X
    max_IG = 0
    var_to_split = None

    #Calculate information gain to find out which variable to split on
    for x in X_dict.keys():
        IG = InfoGain(Y, X_dict[x])
        if IG > max_IG:
            max_IG = IG
            var_to_split = x

    #See if all variables have been used and none are left.
    if var_to_split == None:
        Y_options = list(set(Y))
        tot = float(len(Y))
        count = [0 for _ in range(len(Y_options))]

        for op in range(len(Y_options)):
            for i in range(len(Y)):
                if Y[i] == op:
                    count[op] += 1
        #Format Node label
        Prob = ""
        for op in range(len(Y_options) - 1):
            Prob += "P("
            Prob += str(Y_options[op]) + ")-> "
            P = float(count[op]) / tot
            Prob += "{0:.2f}".format(P)
        #Make a new node
        nodename = node(Prob, color = "orange")
        edge(previous_node, nodename)
    else:
        print("Splitting on {0}".format(var_to_split))
        X_options = list(set(X_dict[var_to_split]))
        #Make decision variable node
        Var_nodename = node(var_to_split, color = "red")
        edge(previous_node, Var_nodename)
        #Init new data for each new branch of the tree
        for X_option in X_options:
            X_nodename = node(str(X_option))
            edge(Var_nodename, X_nodename)
            New_X_dict = {}
            #get remaining variables
            for key in X_dict.keys():
                if key != var_to_split:
                    New_X_dict[key] = []
            New_Y = []
            #Populate
            for i in range(len(Y)):
                if X_dict[var_to_split][i] == X_option:
                    New_Y.append(Y[i])
                    for key in New_X_dict.keys():
                        New_X_dict[key].append(X_dict[key][i])

            #Check if this is a terminal node:
            if len(set(New_Y)) == 1:
                nodename = node(str(New_Y[0]), color = "green")
                edge(X_nodename, nodename)
            else:
                #No terminal node, so try again
                decide(New_Y, New_X_dict, X_nodename)

Y, X_dict =  import_golf('golf.csv')
root_node = node("root", color = "blue")
decide(Y, X_dict, root_node)
filename = g.render(filename='Tree')
print("Done")
