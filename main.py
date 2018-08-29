import math
import random
import operator
import sys



# Function to calculate Entropy. pos is list of positive instances and similarly neg
def entropy(pos,neg):
	p=len(pos)
	n=len(neg)
	if p==0 or n==0:
		return 0
	return ((p+n)*math.log(p+n,2)-p*math.log(p,2)-n*math.log(n,2))/(p+n)



# Function to select attribute which has maximum Information Gain
def max_infogain_attr(attributes,pos,neg):
	# Variable to store maximum IG
	maxig=0
	# Variable to store attribute which has maximum IG currently
	maxig_attr=-1
	# List to store positive instances which don't have maxIG attribute present
	maxig_attr_pos1=[]
	# List to store negative instances which don't have maxIG attribute present
	maxig_attr_neg1=[]
	# List to store positive instances which have maxIG attribute present
	maxig_attr_pos2=[]
	# List to store negative instances which have maxIG attribute present
	maxig_attr_neg2=[]

	# Entropy before splitting
	initial_entropy=entropy(pos,neg)
	for i in attributes:
		pos1=[]
		neg1=[]
		pos2=[]
		neg2=[]
		# Splitting instances based on attribute presence
		for x in pos:
			if i in x:
				pos2.append(x)
			else:
				pos1.append(x)
		for x in neg:
			if i in x:
				neg2.append(x)
			else:
				neg1.append(x)

		entropy1=entropy(pos1,neg1)
		entropy2=entropy(pos2,neg2)

		ig=initial_entropy-((len(pos1)+len(neg1))*entropy1+(len(pos2)+len(neg2))*entropy2)/(len(pos)+len(neg))

		if ig>maxig:
			maxig=ig
			maxig_attr=i
			maxig_attr_pos1=pos1
			maxig_attr_neg1=neg1
			maxig_attr_pos2=pos2
			maxig_attr_neg2=neg2

	return [maxig_attr,maxig_attr_pos1,maxig_attr_neg1,maxig_attr_pos2,maxig_attr_neg2,maxig]




attributes_frequency = {}

# DECISION TREE IMPLEMENTATION
class Node:
	def __init__(self, key):
		self.attr = key
		self.no = None
		self.yes = None
		self.label = None

# ID3 ALGORITHM IMPLEMENTATION
def ID3(attributes,pos,neg,Tnodes=0,Nodes=0):
	# If only positive instances are present
	if len(neg)==0 and len(pos)>0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='Positive'
		return root,Tnodes,Nodes

	# If only negative instances are present
	if len(pos)==0 and len(neg)>0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='Negative'
		return root,Tnodes,Nodes

	# If list of instances are empty
	if len(pos)==0 and len(neg)==0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='None'
		return root	,Tnodes,Nodes

	# temp will store attribute which has max IG and splitted instances based on it
	temp = max_infogain_attr(attributes,pos,neg)
	# If all attributes has zero IG
	if temp[0]==-1:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		if len(pos)>len(neg):
			root.label='Positive'
		elif len(neg)>len(pos):
			root.label='Negative'
		else:
			root.label='None'
		return root,Tnodes,Nodes

	global attributes_frequency
	root = Node(temp[0])
	Nodes+=1
	if temp[0] in attributes_frequency:
		attributes_frequency[temp[0]]+=1
	else:
		attributes_frequency[temp[0]]=1

	if len(pos)>len(neg):
		root.label='Positive'
	elif len(neg)>len(pos):
		root.label='Negative'
	else:
		root.label='None'
	# Remove current attribute from the list of attributes and start spliiting based on remaining attributes
	new_attributes = attributes.copy()
	new_attributes.remove(temp[0])
	# Subtree for instances which don't have max IG attribute present
	root.no,Tnodes,Nodes = ID3(new_attributes,temp[1],temp[2],Tnodes,Nodes)
	# Subtree for instances which have max IG attribute present
	root.yes,Tnodes,Nodes = ID3(new_attributes,temp[3],temp[4],Tnodes,Nodes)

	return root,Tnodes,Nodes






# Function to do Testing
def test(root,data):
	if root.attr==-1:
		return root.label

	if root.attr in data:
		return test(root.yes,data)
	else:
		return test(root.no,data)

# Function to calculate Accuracy
def accuracy(dtree,test_pos,test_neg):
	count=0
	for x in test_pos:
		if test(dtree,x)=='Positive':
			count+=1

	for x in test_neg:
		if test(dtree,x)=='Negative':
			count+=1

	return count*100/(len(test_pos)+len(test_neg))







# EARLY STOPPING


# ID3 EARLY STOPPING (based on maximum depth and min IG) ALGORITHM IMPLEMENTATION
def ID3_early_stopping(attributes,pos,neg,max_d,min_ig,d=0,Tnodes=0,Nodes=0):
	# If only positive instances are present
	if len(neg)==0 and len(pos)>0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='Positive'
		return root,Tnodes,Nodes

	# If only negative instances are present
	if len(pos)==0 and len(neg)>0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='Negative'
		return root,Tnodes,Nodes

	# If list of instances are empty
	if len(pos)==0 and len(neg)==0:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		root.label='None'
		return root,Tnodes,Nodes

	# temp will store attribute which has max IG and splitted instances based on it
	temp = max_infogain_attr(attributes,pos,neg)
	# If all attributes has zero IG or Maximum allowed depth has been reached or IG is less than threshold
	if temp[0]==-1 or d>=max_d or temp[5]<min_ig:
		root=Node(-1)
		Tnodes+=1
		Nodes+=1
		if len(pos)>len(neg):
			root.label='Positive'
		elif len(neg)>len(pos):
			root.label='Negative'
		else:
			root.label='None'
		return root,Tnodes,Nodes

	root = Node(temp[0])
	Nodes+=1

	# Remove current attribute from the list of attributes and start spliiting based on remaining attributes
	new_attributes = attributes.copy()
	new_attributes.remove(temp[0])
	# Subtree for instances which don't have max IG attribute present
	root.no,Tnodes,Nodes = ID3_early_stopping(new_attributes,temp[1],temp[2],max_d,min_ig,d+1,Tnodes,Nodes)
	# Subtree for instances which have max IG attribute present
	root.yes,Tnodes,Nodes = ID3_early_stopping(new_attributes,temp[3],temp[4],max_d,min_ig,d+1,Tnodes,Nodes)
	return root,Tnodes,Nodes



def addnoise(pos,neg,percentage):
	# Switching labels of equal positive and negatives to add noise
	n_pos = math.ceil(percentage*(len(pos)+len(neg))/200)
	n_neg = math.floor(percentage*(len(pos)+len(neg))/200)
	
	temp_p = []
	for i in random.sample(range(len(pos)),n_pos):
		temp_p.append(pos[i])

	temp_n = []
	for i in random.sample(range(len(neg)),n_neg):
		temp_n.append(neg[i])

	for x in temp_p:
		pos.remove(x)
		neg.append(x)

	for x in temp_n:
		neg.remove(x)
		pos.append(x)

	return pos,neg







# RANDOM FOREST IMPLEMENTATION
def RandomForest(attributes,pos,neg,no_of_trees):
	tree_roots = []
	# Choosing d/2.5 random attributes for each tree
	a = len(attributes)/2.5
	for i in range(no_of_trees):
		random_attributes = []
		for j in random.sample(range(0,len(attributes),2),math.ceil(a/2)):
			random_attributes.append(attributes[j])
		for j in random.sample(range(1,len(attributes),2),math.ceil(a/2)):
			random_attributes.append(attributes[j])
			
		tree,Tnodes,Nodes = ID3(random_attributes,pos,neg)
		tree_roots.append(tree)

	return tree_roots


# Function to calculate accuracy in case of random forest
def rforest_accuracy(trees,test_pos,test_neg):
	count=0
	for x in test_pos:
		output=0
		for dtree in trees:
			if test(dtree,x)=='Positive':
				output+=1
			elif test(dtree,x)=='Negative':
				output-=1
		if output>0:
			count+=1


	for x in test_neg:
		output=0
		for dtree in trees:
			if test(dtree,x)=='Positive':
				output+=1
			elif test(dtree,x)=='Negative':
				output-=1
		if output<0:
			count+=1

	return count*100/(len(test_pos)+len(test_neg))








# DECISION TREE PRUNING
def find_max_accuracy_pruning(dtree,node,test_pos,test_neg,max_accu):
	# Checking if node is not a leaf node
	if node.attr != -1:
		left_subtree = node.no
		right_subtree = node.yes
		attr = node.attr
		node.no = None
		node.yes = None
		node.attr = -1
		# Checking accuracy after removal of a subtree
		current_accuracy = accuracy(dtree,test_pos,test_neg)
		if current_accuracy > max_accu:
			max_accu = current_accuracy
		node.no = left_subtree
		node.yes = right_subtree
		node.attr = attr
		
		# Recursively Traversing in preorder and checking accuracy after removal of subtree below each node
		left_max_accuracy = find_max_accuracy_pruning(dtree,node.no,test_pos,test_neg,max_accu)
		if left_max_accuracy > max_accu:
			max_accu = left_max_accuracy

		right_max_accuracy = find_max_accuracy_pruning(dtree,node.yes,test_pos,test_neg,max_accu)
		if right_max_accuracy > max_accu:
			max_accu = right_max_accuracy

		# If max_accuracy is due to removal of current subtree then removing this subtree
		if current_accuracy == max_accu:
			node.no = None
			node.yes = None
			node.attr = -1

	return max_accu



def Dtree_Pruning(dtree,test_pos,test_neg):
	# Initializing max accuracy with initial accuracy
	max_accu = accuracy(dtree,test_pos,test_neg)
	# Removing a subtree which results in max accuracy
	current_accu = find_max_accuracy_pruning(dtree,dtree,test_pos,test_neg,max_accu)
	# Do pruning until accuracy increases
	while current_accu>max_accu:
		max_accu = current_accu
		current_accu = find_max_accuracy_pruning(dtree,dtree,test_pos,test_neg,max_accu)


def calculate_nodes(dtree,nodes=0):
	if dtree.attr!=-1:
		nodes = calculate_nodes(dtree.no,nodes)
		nodes = calculate_nodes(dtree.yes,nodes)
	return nodes+1


if len(sys.argv)!=4:
	print('Please run in proper format. i.e.\n\tmain.py PATH_TO_TRAINING_DATA_FILE PATH_TO_TESTING_DATA_FILE EXPERIMENT_NUMBER')

else:
	# TRAINING DATA READING
	# pos will store positive training instances and similarly neg
	pos = []
	neg = []
	file = open(str(sys.argv[1]),'r')
	trdata = file.read().split('\n')
	if '' in trdata:
		trdata.remove('')
	file.close()

	for x in trdata:
		a = x.split(' ')
		temp={}
		for i in range(1,len(a)):
			b=a[i].split(':')
			temp[int(b[0])]=int(b[1])
		if int(a[0])>=7:
			pos.append(temp)
		else:
			neg.append(temp)

	trdata.clear()



	# SELECTED FEATURE INDICES READING FROM 'selected-features-indices.txt'
	file = open('selected-features-indices.txt','r')
	attributes=file.read().split('\n')
	if '' in attributes:
	 	attributes.remove('')
	file.close()
	for i in range(0,len(attributes)):
		attributes[i]=int(attributes[i])

	

	# TEST DATA READING
	test_pos = []
	test_neg = []
	file = open(str(sys.argv[2]),'r')
	trdata = file.read().split('\n')
	if '' in trdata:
		trdata.remove('')
	file.close()

	for x in trdata:
		a = x.split(' ')
		temp={}
		for i in range(1,len(a)):
			b=a[i].split(':')
			temp[int(b[0])]=int(b[1])
		if int(a[0])>=7:
			test_pos.append(temp)
		else:
			test_neg.append(temp)

	trdata.clear()


	# Experiments
	if int(sys.argv[3]) == 2:
		print('Please Wait ...')
		attributes_frequency = {}
		# Normal Decision Tree
		dtree,Tnodes,Nodes = ID3(attributes,pos,neg)
		# Early Stopping with max depth = 70 and min IG = 0.001
		dtree1,Tnodes1,Nodes1 = ID3_early_stopping(attributes,pos,neg,70,0.001)
		print('\nNumber of times an attribute is used as the splitting function\nIndex\tCount')
		for k,v in sorted(attributes_frequency.items(), key=operator.itemgetter(1),reverse=True):
			if v<2:
				break
			print(str(k)+'\t'+str(v))
		print('\n\n\t\t\tNormal\tEarly Stopping')
		print('Total Nodes\t\t'+str(Nodes)+'\t'+str(Nodes1))
		print('Terminal Nodes\t\t'+str(Tnodes)+'\t'+str(Tnodes1))
		print('Training Accuracy\t'+str(accuracy(dtree,pos,neg))+'\t'+str(accuracy(dtree1,pos,neg)))
		print('Testing Accuracy\t'+str(accuracy(dtree,test_pos,test_neg))+'\t'+str(accuracy(dtree1,test_pos,test_neg)))



	elif int(sys.argv[3]) == 3:
		print('Please Wait, It may take several minutes')
		attributes_frequency = {}
		# Without Noise
		dtree,Tnodes,Nodes = ID3(attributes,pos,neg)
		
		# With 0.5% Noise
		pos1 = pos.copy()
		neg1 = neg.copy()
		pos1,neg1 = addnoise(pos1,neg1,0.5)
		dtree1,Tnodes1,Nodes1 = ID3(attributes,pos1,neg1)

		# With 1% Noise
		pos2 = pos.copy()
		neg2 = neg.copy()
		pos2,neg2 = addnoise(pos2,neg2,1)
		dtree2,Tnodes2,Nodes2 = ID3(attributes,pos2,neg2)

		# With 5% Noise
		pos3 = pos.copy()
		neg3 = neg.copy()
		pos3,neg3 = addnoise(pos3,neg3,5)
		dtree3,Tnodes3,Nodes3 = ID3(attributes,pos3,neg3)

		# With 0.5% Noise
		pos4 = pos.copy()
		neg4 = neg.copy()
		pos4,neg4 = addnoise(pos4,neg4,10)
		dtree4,Tnodes4,Nodes4 = ID3(attributes,pos4,neg4)

		print('\n\nNoise\t\t\t0%\t0.5%\t1%\t5%\t10%')
		print('Total Nodes\t\t'+str(Nodes)+'\t'+str(Nodes1)+'\t'+str(Nodes2)+'\t'+str(Nodes3)+'\t'+str(Nodes4))
		print('Terminal Nodes\t\t'+str(Tnodes)+'\t'+str(Tnodes1)+'\t'+str(Tnodes2)+'\t'+str(Tnodes3)+'\t'+str(Tnodes4))
		print('Training Accuracy\t'+str(accuracy(dtree,pos,neg))+'\t'+str(accuracy(dtree1,pos,neg))+'\t'+str(accuracy(dtree2,pos2,neg2))+'\t'+str(accuracy(dtree3,pos3,neg3))+'\t'+str(accuracy(dtree4,pos4,neg4)))
		print('Testing Accuracy\t'+str(accuracy(dtree,test_pos,test_neg))+'\t'+str(accuracy(dtree1,test_pos,test_neg))+'\t'+str(accuracy(dtree2,test_pos,test_neg))+'\t'+str(accuracy(dtree3,test_pos,test_neg))+'\t'+str(accuracy(dtree4,test_pos,test_neg)))


	elif int(sys.argv[3]) == 4:
		print('Please Wait, It may take several minutes')
		attributes_frequency = {}
		dtree,Tnodes,Nodes = ID3(attributes,pos,neg)
		print('\tInitial Nodes = '+str(Nodes))
		print('Initial Training Accuracy = '+str(accuracy(dtree,pos,neg)))
		print('Initial Testing Accuracy = '+str(accuracy(dtree,test_pos,test_neg)))
		Dtree_Pruning(dtree,test_pos,test_neg)
		print('Final Nodes = '+str(calculate_nodes(dtree)))
		print('Final Training Accuracy = '+str(accuracy(dtree,pos,neg)))
		print('Final Testing Accuracy = '+str(accuracy(dtree,test_pos,test_neg)))

	elif int(sys.argv[3]) == 5:
		print('Please Wait, It may take long time')
		attributes_frequency = {}
		trees5 = RandomForest(attributes,pos,neg,5)
		print('Trees\tAccuracy')
		print('5\t'+str(rforest_accuracy(trees5,test_pos,test_neg)))
		trees10 = trees5 + RandomForest(attributes,pos,neg,5)
		print('10\t'+str(rforest_accuracy(trees10,test_pos,test_neg)))
		trees20 = trees10 + RandomForest(attributes,pos,neg,10)
		print('20\t'+str(rforest_accuracy(trees20,test_pos,test_neg)))
		trees50 = trees20 + RandomForest(attributes,pos,neg,30)
		print('50\t'+str(rforest_accuracy(trees50,test_pos,test_neg)))

	else:
		print('Please Try again!')