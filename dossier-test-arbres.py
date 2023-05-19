from algo_py import bintree

def __testBST(B : bintree.BinTree, inf : int, sup : int) -> bool:
    if B == None:
        return True

    if B.key <= inf or B.key > sup:
        return False
    
    else:
        return __testBST(B.left, inf, B.key) and __testBST(B.right, B.key, sup);
    
    

def testBST(B):
    return __testBST(B, -infty, infty)
















# =============================================================================== #


E = bintree.BinTree(5, None, None)
D = bintree.BinTree(4, None, None)
C = bintree.BinTree(1, None, None)
B = bintree.BinTree(2, C, D)
A = bintree.BinTree(4, B, E)

infty = float('inf')



print(testBST(A))