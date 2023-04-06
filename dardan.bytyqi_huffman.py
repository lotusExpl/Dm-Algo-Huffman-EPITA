__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2023-03-24'

"""
Huffman homework
2023-03
@author: dardan.bytyqi
"""

from algo_py import bintree
from algo_py import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
# FONCTIONS AUXILIAIRES
    

def __build_dict(huffmanTree : bintree.BinTree): 
    '''
    fonction qui retourne une liste de tuples (char, chemin d'occurence)
    etant un equivalent de dictionnaire pour l'encodage des lettres
    '''
    dico = []
    def build(tree : bintree.BinTree, chemin : str) -> None:
        '''
        fonction chapeau qui ajoute des elements dans le dico
        '''

        if tree.left == None and tree.right == None:
            dico.append((tree.key, chemin))

        if tree.left != None:
            build(tree.left, chemin + '0')
        
        if tree.right != None:
            build(tree.right, chemin + '1')
    
    build(huffmanTree, "")

    return dico;



def __defi(char, dico):
    '''
    retourne le chemin d'occurence d'un charactere
    '''

    i = 0
    while dico[i][0] != char:
        i += 1

    return dico[i][1];



def __binary_to_int(octet):
    '''
    converti un octet en un entier pour une autre fonction
    '''

    res = 0
    pow = 0
    for i in range(len(octet)-1,-1,-1):
        res += (ord(octet[i])-48)*(2**pow)
        pow += 1
    return res;



def __int_to_binary(n : int) -> str:
    '''
    retourne le code binaire d'un entier sur un octet
    '''

    res = ""
    while n != 0:
        res = chr(n % 2 + 48) + res
        n //= 2
    while len(res) != 8:
        res = '0' + res
    return res;



def __slice(txt):
    '''
    retourne une liste d'octet 
    '''

    res = []
    size = len(txt)
    for i in range(0,size // 8):
        octet = ""
        for j in range(0,8):
            octet += txt[i*8 + j]
        res.append(octet)

    reste = ""
    for i in range((size//8)*8,size):
        reste += txt[i]
    
    align = 0
    if reste != "":
        while len(reste) != 8:
            align += 1
            reste = '0' + reste
        res.append(reste)
    
    return (res, align)



     
###############################################################################
## COMPRESSION

def build_frequency_list(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    hist = [];
    for i in range(255):
        hist.append(0);
    for i in dataIN:
        hist[ord(i)] += 1;
    res = [];
    for i in range(255):
        if hist[i] != 0:
            res.append((hist[i], chr(i)));
    return res;



def build_Huffman_tree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """

    H = heap.Heap()
    for elt in inputList:
        H.push((elt[0],bintree.BinTree(elt[1],None,None)))

    while len(H.elts) > 2: #2 car heap commence avec None
        n1 = H.pop()
        n2 = H.pop()
        H.push((n1[0]+n2[0], bintree.BinTree(None, n2[1], n1[1])))

    return H.pop()[1];



def encode_data(huffmanTree : bintree.BinTree, dataIN : str):
    """
    Encodes the input string to its binary string representation.
    """
    dico = __build_dict(huffmanTree)
    res = ""
    for c in dataIN:
        res += __defi(c, dico)
    return res;




def encode_tree(huffmanTree : bintree.BinTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """

    if huffmanTree.left == None and huffmanTree.right == None:
        return '1' + __int_to_binary(ord(huffmanTree.key))
    elif huffmanTree.left != None and huffmanTree.right != None:
        return '0' + encode_tree(huffmanTree.left) + encode_tree(huffmanTree.right)
    elif huffmanTree.left != None:
        return '0' + encode_tree(huffmanTree.left)
    else:
        return '0' + encode_tree(huffmanTree.right)




def to_binary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """

    (data, align) = __slice(dataIN)
    res = ""
        
    for o in data:
        res += chr(__binary_to_int(o))

    return (res , align)




def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    
    huff = build_Huffman_tree(build_frequency_list(dataIn))
    return(to_binary(encode_data(huff, dataIn)), to_binary(encode_tree(huff)))


    
################################################################################
## DECOMPRESSION

def decode_data(huffmanTree : bintree.BinTree, dataIN : str):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """

    res = ""
    pointeur = 0
    tree = huffmanTree
    path = dataIN[0]

    while pointeur < len(dataIN)-1:
        for i in range(len(path)-1):
            if path[i] == '0':
                tree = tree.left 
                
                
            else:
                tree = tree.right
            print(path) 
            print(tree)
            
        if tree != None and tree.key != None:
            res = res + str(tree.key)
            tree = huffmanTree
            path = ""
            # pb dans la maniere de gerer le path
        pointeur += 1
        path += dataIN[pointeur]

    return res

huffman = build_Huffman_tree(build_frequency_list('bbaabtttaabtctce'))

data = encode_data(huffman,'bbaabtttaabtctce' )
print(decode_data(huffman, data))


    
def decode_tree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    
    def __rec_decode_tree(dataIN, pointeur, decalage):
        if dataIN[pointeur] == '0':
            left = __rec_decode_tree(dataIN, pointeur + 1)

        # inserer algo ici

        else:
            feuille = ""
            for i in range(pointeur, pointeur + 8):
                feuille += dataIN[i]
            pointeur += 8
            return bintree.BinTree(chr(__binary_to_int(feuille)), None, None)
    
    return # inserer resultat ici
        




def from_binary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    
    lim = len(dataIN)
    res = ""
    for i in range(lim-1):
        res += __int_to_binary(ord(dataIN[i]))
        
    reste = __int_to_binary(ord(dataIN[lim-1]))
    for i in range(align, 8):
        res += reste[i]
    return res;




def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    # FIXME
    pass




#huff = build_Huffman_tree(build_frequency_list('bbaabtttaabtctce'))
#print(huff)
#print(encode_data(huff, 'bbaabtttaabtctce'))
#print(to_binary('01011010010000001010010011000110111'))

#print(to_binary("01011010010000001010010011000110111"))
#build_Huffman_tree(build_frequency_list("bbaabtttaabtctce"))
#print(to_binary("10100101000000010000110101100011111"))
#huff = build_Huffman_tree(build_frequency_list('ZELIUfbmozefn'))
#print(huff)
#print(encode_tree(huff))
#print(encode_data(huff, 'ZELIUfbmozefn'))