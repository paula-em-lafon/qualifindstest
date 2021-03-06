# Tree Code

class Node:
	def  __init__(self, data):
		self.data = data
		self.parent = None
		self.left = None
		self.right = None
		self.bf = 0

class AVLTree:
    def __init__(self):
        self.root = None    
    def __searchTreeHelper(self, node, key):
    	if node == None or key == node.data:
    		return node 
    	if key < node.data:
    		return self.__searchTreeHelper(node.left, key)
    	return self.__searchTreeHelper(node.right, key)

    	# update the balance factor the node
    def __updateBalance(self, node):
    	if node.bf < -1 or node.bf > 1:
    		self.__rebalance(node)
    		return  
    	if node.parent != None:
    		if node == node.parent.left:
    			node.parent.bf -= 1 
    		if node == node.parent.right:
    			node.parent.bf += 1 
    		if node.parent.bf != 0:
    			self.__updateBalance(node.parent)   
     # rebalance the tree
    def __rebalance(self, node):
    	if node.bf > 0:
    		if node.right.bf < 0:
    			self.rightRotate(node.right)
    			self.leftRotate(node)
    		else:
    			self.leftRotate(node)
    	elif node.bf < 0:
    		if node.left.bf > 0:
    			self.leftRotate(node.left)
    			self.rightRotate(node)
    		else:
    			rightRotate(node)

    # search the tree for the key k
    # and return the corresponding node
    def searchTree(self, k):
    	return self.__searchTreeHelper(self.root, k)

    # rotate left at node x
    def leftRotate(self, x):
    	y = x.right
    	x.right = y.left
    	if y.left != None:
    		y.left.parent = x   
    	y.parent = x.parent
    	if x.parent == None:
    		self.root = y
    	elif x == x.parent.left:
    		x.parent.left = y
    	else:
    		x.parent.right = y
    	y.left = x
    	x.parent = y    
    	# update the balance factor
    	x.bf = x.bf - 1 - max(0, y.bf)
    	y.bf = y.bf - 1 + min(0, x.bf)  
    # rotate right at node x
    def rightRotate(self, x):
    	y = x.left
    	x.left = y.right
    	if y.right != None:
    		y.right.parent = x
    
    	y.parent = x.parent
    	if x.parent == None:
    		self.root = y
    	elif x == x.parent.right:
    		x.parent.right = y
    	else:
    		x.parent.left = y
    
    	y.right = x
    	x.parent = y    
    	# update the balance factor
    	x.bf = x.bf + 1 - min(0, y.bf)
    	y.bf = y.bf + 1 + max(0, x.bf)  
    # insert the key to the tree in its appropriate position
    def insert(self, key):
    	# PART 1: Ordinary BST insert
    	node =  Node(key)
    	y = None
    	x = self.root   
    	while x != None:
    		y = x
    		if node.data < x.data:
    			x = x.left
    		else:
    			x = x.right 
    	# y is parent of x
    	node.parent = y
    	if y == None:
    		self.root = node
    	elif node.data < y.data:
    		y.left = node
    	else:
    		y.right = node  
    	# PART 2: re-balance the node if necessary
    	self.__updateBalance(node)  