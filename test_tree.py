import sys
sys.setrecursionlimit(10**8)
from hypothesis import given
from hypothesis.strategies import integers, lists
from naive_algo import *
import random

count = 1

def create_random_tree(seed):
    random.seed(seed)
    def rec_tree(depth):
        global count
        if random.random() < 0.2 or depth > 3:
            count += 1
            return Leaf(count)
        else:
            return Node(rec_tree(depth+1),rec_tree(depth+1),rec_tree(depth+1))
    return rec_tree(0)

def triplet_complement(leafs,triplets):
    c = Set()
    for i in leafs:
        for j in leafs:
            for k in leafs:
                if i<j:
                    c.add( ((i,j),k) )
    for t in triplets:
        c.remove(t)
    return c.get_all()

def test_create_tree():
    l1 = Leaf(1)
    l2 = Leaf(2)
    l3 = Leaf(3)
    n1 = Node(l1,l2)
    n2 = Node(n1,l3)
    assert n2.l.l.name == 1
    assert n2.l.r.name == 2
    assert n2.r.name == 3

def test_compute_clusters():
    l1 = Leaf(1)
    l2 = Leaf(2)
    l3 = Leaf(3)
    l4 = Leaf(4)
    l5 = Leaf(5)
    n1 = Node(l1,l2)
    n2 = Node(l3,l4)
    n3 = Node(n1,l5)
    n4 = Node(n3,n2)
    n4.compute_cluster()
    assert l1.cluster == Set([1])
    assert l2.cluster == Set([2])
    assert l3.cluster == Set([3])
    assert l4.cluster == Set([4])
    assert l5.cluster == Set([5])
    assert n1.cluster == Set([1,2])
    assert n2.cluster == Set([3,4])
    assert n3.cluster == Set([1,2,5])
    assert n4.cluster == Set([1,2,5,3,4])

def test_couples():
    l1 = Leaf(1)
    l2 = Leaf(2)
    l3 = Leaf(3)
    l4 = Leaf(4)
    l5 = Leaf(5)
    n1 = Node(l1,l2)
    n2 = Node(l3,l4)
    n3 = Node(n1,l5)
    n4 = Node(n3,n2)
    assert n1.get_couples() == Set([(1,2)])
    assert n2.get_couples() == Set([(3,4)])
    assert n3.get_couples() == Set([(1,2),(1,5),(2,5)])
    assert n4.get_couples() == Set([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)])

def test_has_triplets():
    l1 = Leaf(1)
    l2 = Leaf(2)
    l3 = Leaf(3)
    l4 = Leaf(4)
    l5 = Leaf(5)
    n1 = Node(l1,l2)
    n2 = Node(l3,l4)
    n3 = Node(n1,l5)
    n4 = Node(n3,n2)
    assert n4.has_triplet(((1,2),4))
    assert n4.has_triplet(((1,2),3))
    assert not(n4.has_triplet(((1,3),2)))
    
def test_has_triplets2():
    l1 = Leaf(1)
    l2 = Leaf(2)
    l3 = Leaf(3)
    l4 = Leaf(4)
    l5 = Leaf(5)
    n1 = Node(l1,l2,l3)
    n2 = Node(n1,l4)
    n3 = Node(n2,l5)
    assert n3.has_triplet(((1,2),4))
    assert not(n3.has_triplet(((1,4),2)))

def test_triplets_random_tree():
    tree = create_random_tree(42)
    print(tree)
    triplets = tree.get_triplets()
    print("check",len(triplets),"\n")
    for index,t in enumerate(triplets):
        if index%100000==0:
            print(index)
        assert tree.has_triplet(t)
    print("comp\n")
    triplets_comp = triplet_complement(tree.cluster.get_all(),triplets)
    print("check",len(triplets_comp),"\n")
    for index,t in enumerate(triplets_comp):
        if index%100000==0:
            print(index)
        assert not(tree.has_triplet(t))

def test_sym_diff():
    l1 = [2,4,5,7,12,15]
    l2 = [3,1,2,5]
    print(sym_dif(l1,l2))
    assert sym_dif(l1,l2) == Set([4,7,12,15,3,1])

test_triplets_random_tree()
