""" Un triplet est un tuple de 3 elements ((a,b),c) representant ab|c car en terme de factorisation du code c'est algorithmiquement plus interessant. Il est cependant possible d'avoir un triplet (a,b,c) en cas d'incertitude"""


class Set:
    def __init__(self,li=[]):
        self.l = {}
        for i in li:
            self.l[i] = None
    def add(self,e):
        self.l[e] = None
    def remove(self,e):
        try:
            del self.l[e]
        except KeyError:
            pass
    def merge(self,s):
        s.l.copy()
        self.l.update(s.l)
    def contains(self,e):
        try:
            self.l[e]
            return True
        except KeyError:
            return False
    def contains_list(self,l):
        for i in l:
            if not(self.contains(i)):
                return False
        return True
    def get_all(self):
        return list(self.l.keys())
    def __str__(self):
        return "{"+(str(self.l)[1:-1])+"}"
    def __add__(self,s2):
        s = Set()
        s.merge(self)
        s.merge(s2)
        return s
    def __eq__(self,s):
        return self.l == s.l

class TripletSet(Set):
    def contains(self,e):
        
        try:
            s[e]
            return True
        except KeyError:
            try:
                try:
                    ((a,b),c) = e
                    s[(a,b,c)]
                except ValueError:
                    (a,b,c) = e
                    s[((a,b
                return True
            except KeyError:
                return False

class Leaf:
    def __init__(self,name):
        self.name = name
        self.cluster = Set([name])
        self.cluster_computed = True
    def __str__(self):
        return "Leaf("+str(self.name)+")"
    def get_couples(self):
        return Set()
    def get_triplets(self):
        return []

class Node:
    def __init__(self,l,r,m=None):
        self.cluster = Set()
        self.cluster_computed = False
        self.l = l
        self.r = r
        self.m = m
        self.children = [l,m,r]
        
    def compute_cluster(self):
        """  O(n) time and space"""
        self.cluster = Set()
        for child in self.children:
            if not(child is None):
                if not(child.cluster_computed):
                    child.compute_cluster()
                self.cluster.merge(child.cluster)
        self.cluster_computed = True
        
    def get_couples(self):
        """ O(n^2) time and space """
        self.compute_cluster()
        return prod(self.cluster,self.cluster)
        
    def get_triplets(self):
        """ We assume the arity of the tree is <= 3 (bounded), in this case, O(n^3) time and space"""
        self.compute_cluster()
        inter_triplets = Set()
        for i,child in enumerate(self.children):
            for j,child2 in enumerate(self.children):
                if i != j and child != None and child2 != None:
                    inter_triplets.merge( prod(child.get_couples(),child2.cluster) )
        uncertain_triplets = Set()
        for i,child in enumerate(self.children):
            for j,child2 in enumerate(self.children):
                for k,child3 in enumerate(self.children):
                    if i < j and j < k and not(child is None) and not(child2 is None) and not(child3 is None):
                        flat_triplets.merge( prod(child.cluster,child2.cluster,child3.cluster) )
        solo_triplets = []
        for child in self.children:
            if child != None:
                solo_triplets += child.get_triplets()
        return inter_triplets.get_all() + uncertain_triplets.get_all() + solo_triplets
        
    def has_triplet(self,triplet): #Debug function (algorithmically bad)
        """ Bad """
        self.compute_cluster()
        ((a,b),c) = triplet
        list_triplet = [a,b,c]
        if len(self.cluster.get_all()) < 3:
            return False
        for child in self.children:
            if not(child is None) and child.cluster.contains_list(list_triplet): #On ne demandera jamais ça a une feuille avec la condition precedente
            	return child.has_triplet(triplet)
        for i,child in enumerate(self.children):
            for j,child2 in enumerate(self.children):
                if not(child is None) and not(child2 is None):
                    if child.cluster.contains_list(list(triplet[0])) and child2.cluster.contains(triplet[1]):
                        return True
        return False
            
    def __str__(self):
        return "Node("+str(self.l)+","+str(self.r)+")"
        
def prod(l1,l2,l3=None):
    """ O(len(l1)*len(l2)) time and space """
    couples = Set()
    for i in l1.get_all():
        for j in l2.get_all():
            if l3 is None:
                if type(i) != type(j) or i<j:
                    couples.add( (i,j) )
                elif j<i:
                    couples.add( (j,i) )
            else:
                for k in l3.get_all():
                    l = [i,j,k]
                    l.sort()
                    [a,b,c] = l
                    couples.add( (a,b,c) )
            
    return couples

def sym_dif(l1,l2):
    """ O(len(l1) + len(l2)) time and space) """
    def difference(l,s):
        diff = Set()
        for e in l:
            if not(s.contains(e)):
                diff.add(e)
        return diff
    s = difference(l1,TripletSet(l2))
    print(s)
    s.merge(difference(l2,TripletSet(l1)))
    return s

def nb_diff_triplets(t1,t2):
    sd = sym_dif(t1.get_triplets(),t2.get_triplets())
    return len(sd.get_all()),sd

def parseur(txt):
    def security(txt):
        for x in txt:
            if not(x in ["(",")",",","0","1","2","3","4","5","6","7","8","9","\n"]):
                print("Error : incorrect char ->"+x+"<-")
                assert False #Incorrect char
    security(txt)
    txt2 = "("
    buff = ""
    for c in txt:
        if c == "(":
            txt2 += "Node("
        elif c in ["0","1","2","3","4","5","6","7","8","9"]:
            buff += c
        elif c == "\n":
            txt2 += ","
        else:
            if buff == "":
                txt2 += c
            else:
                txt2 += "Leaf("+buff+")"+c
                buff = ""
    txt2 += ")"
    return eval(txt2)

def triplets():
    f = open("test1.txt")
    txt = f.read()
    print("TEXT:",txt)
    (tree1,tree2) = parseur(txt)
    print("TREE1",tree1)
    print("TREE2",tree2)
    nb,s = nb_diff_triplets(tree1,tree2)
    print("FINAL SET",s)
    return nb

print(triplets())
