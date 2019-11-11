#A triplet is a tuple of dimension 5 : (a,b,c,pos,unsure) where a,b,c are leaves sorted in the lexicographic order, pos is the position in [a,b,c] of the separated leaf (for example if pos == 1, it's b|ac). Eventually unsure means if the triplet is of type a|b|c and in that case for a slightly better complexity, pos = 0 (and is useless).

class TripletSet():
    """ It represents a set of triplets, it needs to be able to efficiently see if a triplet belongs to the set and especially handle the fact that some of them are unsure """
    def __init__(self,li=[]):
        """ init function from a list """
        self.l = {}
        for i in li:
            self.l[i] = None
    def add(self,e):
        """ adds a triplet to the set """
        self.l[e] = None
    def remove(self,e):
        """ removes a specific triplet (won't check if one is unsure and could be removed, you need to be specific when you use this function) """
        try:
            del self.l[e]
        except KeyError:
            pass
    def merge(self,s):
        """ Merge an other set into this set """
        s.l.copy()
        self.l.update(s.l)
    def contains(self,e):
        """ Check if it contains a triplet e """
        (a,b,c,pos,unsure) = e
        try: #Check if it is directly in the set
            self.l[e]
            return True
        except KeyError: #If it's not the case there are 2 possibilities depending on whether it's a unsure triplet
            if unsure: #If it's an unsure triplet
                for p in range(3): #It will try every sure triplet associated to it (the data structure allows us to do it in 3 tests)
                    try:
                        self.l[(a,b,c,p,False)]
                        return True
                    except KeyError:#The return False is at the end of the function
                        pass
            else:#If it's not
                try:#It means our triplet is sure but hasn't been found directly so it'll check if there is an unsure triplet corresponding to it in the set
                    self.l[(a,b,c,0,True)]
                    return True
                except KeyError:#The return False is at the end of the function
                    pass
            return False

    def contains_list(self,l):
        """ Same function but for lists """
        for i in l:
            if not(self.contains(i)):
                return False
        return True
    def get_all(self):
        """ Returns a list of all triplets """
        return list(self.l.keys())
    def __str__(self):
        """ To print it correctly """
        return "{"+(str(self.l)[1:-1])+"}"
    def __add__(self,s2):
        """ To merge with an other syntax """
        s = Set()
        s.merge(self)
        s.merge(s2)
        return s
    def __eq__(self,s):
        """ To check whether 2 sets are equal """
        return self.l == s.l

class Leaf:
    """ Leafs of the phylogenetic tree """
    def __init__(self,name):
        """ init function storing the same and computing the trivial cluster """
        self.name = name
        self.cluster = [name]
        self.cluster_computed = True
    def __str__(self):
        """ To print it correctly """
        return "Leaf("+str(self.name)+")"
    def get_triplets(self):
        """ A Leaf has no triplets """
        return []

class Node:
    def __init__(self,l,r,m=None):
        """ init function, using at least 2 parameters : left and right children and one optional : the middle child if there is one """
        self.cluster = []
        self.cluster_computed = False #The cluster isn't computed yet
        self.l = l
        self.r = r
        self.m = m
        self.children = [l,m,r] #The list of children
        
    def compute_cluster(self):
        """  Computes the cluster of this node : O(n) time and space"""
        self.cluster = []
        for child in self.children:
            if not(child is None):
                if not(child.cluster_computed):
                    child.compute_cluster()
                self.cluster += child.cluster
        self.cluster_computed = True
        
    def get_triplets(self):
        """ We assume the arity of the tree is <= 3 (bounded), in this case, O(n^3) time and space multiplied by a O(log n) because we store values in a set"""
        self.compute_cluster() #First we compute the cluster if it hasn't been computed yet
        inter_triplets = TripletSet() #Computation of the inter_triplet which is the set of triplets from which the least common ancestor is this node (2 leaves in one child and 1 in an other).
        for i,child in enumerate(self.children):
            for j,child2 in enumerate(self.children):
                if i != j and child != None and child2 != None:
                    inter_triplets.merge(create_triplets(child2.cluster,child.cluster,child.cluster,False))
        uncertain_triplets = TripletSet() #Computation of uncertain triplets (those like a|b|c) which the least common ancestor is this node
        for i,child in enumerate(self.children):
            for j,child2 in enumerate(self.children):
                for k,child3 in enumerate(self.children):
                    if i < j and j < k and not(child is None) and not(child2 is None) and not(child3 is None):
                        uncertain_triplets.merge(create_triplets(child.cluster,child2.cluster,child3.cluster,True))
        solo_triplets = [] #Computation of triplets that are included in one child
        for child in self.children:
            if child != None:
                solo_triplets += child.get_triplets()
        return inter_triplets.get_all() + uncertain_triplets.get_all() + solo_triplets #Returns all computed triplets
            
    def __str__(self):
        """ To print it correctly """
        return "Node("+str(self.l)+","+str(self.m)+","+str(self.r)+")"

def create_triplets(l1,l2,l3,bo):
    """ Transforms a lists of a, a list of b, a list of c and a boolean into a list of triplets representing a|bc (if bo=False) or a|b|c (if bo=True) : O(len(l1)*len(l2)*len(l3)) time and space -> but len(l1),len(l2),len(l3)<nb_nodes so in O(n^3)"""
    triplets = TripletSet()
    for i in l1:
        for j in l2:
            for k in l3:
                if i != j and j != k and i != k: #A triplet cannot have 2 same leaves in it
                    l = [i,j,k] #Computing pos -> sort [i,j,k] (representing i|jk) and pos is the new position of i in the sorted list
                    l.sort()
                    [a,b,c] = l
                    pos = l.index(i)
                    if bo: #If it's an unsure triplet, pos = 0
                        pos = 0
                    triplets.add((a,b,c,pos,bo))
    return triplets

def sym_dif(l1,l2):
    """ Compute the symetric difference between 2 lists of leaves l1 and l2 : O(len(l1)*log(len(l2)) + len(l2)*log(len(l1))) time and space -> O(log(n)*n^3) """
    def difference(l,s):
        """ Compute the difference between leaves in the list l and leaves in the set s """
        diff = TripletSet()
        for e in l:
            if not(s.contains(e)):
                diff.add(e)
        return diff
    diff = difference(l1,TripletSet(l2)) #Compute both difference to reconstruct the symmetric difference
    diff.merge(difference(l2,TripletSet(l1)))
    return diff.get_all()

def nb_diff_triplets(t1,t2):
    """ Compute the number of different triplets between tree1 and tree2 """
    sd = sym_dif(t1.get_triplets(),t2.get_triplets())
    return len(sd),sd

def parseur(txt):
    """ Parse the input """
    def is_char(c):
        """ Can be in the name of Leaves (0_9A_Z)"""
        return 48 <= ord(c) and ord(c) <= 57 or 65 <= ord(c) <= 90
    buff = "" #Buffer for the name of Leaves
    pile = [] #Pile of what is currently beeing built
    arity = [] #Arity of nodes in construction
    tree1 = None #To store the first tree when it's building the second one
    for c in txt:
        if c == "(": #Starts a node
            arity.append(0)
        elif is_char(c): #Stores a char in the buffer
            buff += c
        elif c == "\n": #Finish the 1st tree and start working on the second one
            tree1 = pile.pop()
        elif c  == ",": #Creates a Leaf is there is one to be created
            arity[-1] += 1
            if buff != "":
                pile.append(Leaf(buff))
            buff = ""
        elif c == ")": #Creates a Leaf is necessary, then a Node.
            arity[-1] += 1
            if buff != "":
                pile.append(Leaf(buff))
            buff = ""
            if arity[-1] == 2: #Check the arity to build a corresponding Node
                a = pile.pop() #Node of arity 2
                b = pile.pop()
                node = Node(b,a)
            else:
                a = pile.pop() #Node of arity 3
                b = pile.pop()
                c = pile.pop()
                node = Node(c,a,b)
            pile.append(node) #Adds the node to the pile
            arity.pop()
    tree2 = pile.pop() #Get the second tree
    return (tree1,tree2)

def triplets():
    """ Final function to handle test environement input and output files """
    finput = open("input.txt") #Get input
    txt = finput.read()
    finput.close()
    (tree1,tree2) = parseur(txt) #Get trees
    nb,s = nb_diff_triplets(tree1,tree2)
    foutput = open("output.txt","w") #Write ouput
    foutput.write(str(nb))
    foutput.close()
    return nb

print(triplets())
