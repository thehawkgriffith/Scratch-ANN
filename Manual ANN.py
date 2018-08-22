import numpy as np

# Creating a base class for operations 

class Operation():

	# Initialing operation object by a list of input nodes
	# Then appending those input nodes to the output nodes list of that extended class (i.e. Variable or Placeholder)

	def __init__(self, input_nodes = []):
		self.input_nodes = input_nodes
		self.output_nodes = []
		for node in input_nodes:
			node.output_nodes.append(self)

	def compute(self):
		pass

# Creating class add that extends Operation

class add(Operation):

	def __init__(self, x, y):
		super().__init__([x, y])

	#Storing the input values as a list and returning the output value

	def compute(self, x_var, y_var):
		self.inputs = [x_var, y_var]
		return x_var + y_var

# Creating class mul that extends Operation

class mul(Operation):

	def __init__(self, x, y):
		super().__init__([x, y])

	def compute(self, x_var, y_var):
		self.inputs = [x_var, y_var]
		return x_var * y_var

# Creating Placeholders to recieve inputs and store output nodes as a list

class Placeholder():
	
	def __init__(self):
		self.output_nodes = []
		_default_graph.placeholders.append(self)

# Creating Variables to instantiate changeable paremeters of our equation
# Then storing the output nodes as a list

class Variable():

	def __init__(self, initial_value=None):
		self.value = initial_value
		self.output_nodes = []
		_default_graph.variables.append(self)

class Graph():

	def __init__(self):
		self.operations = []
		self.placeholders = []
		self.variables = []

	def set_as_default(self):
		global _default_graph
		_default_graph = self

# Defining a function to conduct the correct flow of order of operations
# Returning a list of operations is a correct order

def traverse_postorder(operation):

	nodes_postorder = []
	def recurse(node):
		if isinstance(node, Operation):
			for input_node in node.input_nodes:
				recurse(input_node)
		nodes_postorder.append(node)
	recurse(operation)
	return nodes_postorder

# Defining a class that has the 'run' method to run our operations as per the correct order

class Session():
	
	# Taking in the oeration and the feed_dict 

	def run(self, operation, feed_dict={}):
		nodes_postorder = traverse_postorder(operation)
		for node in nodes_postorder:
			if type(node) == Placeholder:
				node.output = feed_dict[node]
			elif type(node) == Variable:
				node.output = node.value
			else:
				node.inputs = [input_node.output for input_node in node.input_nodes]
				node.output = node.compute(*node.inputs)
			if type(node.output) == list:
				node.output = np.array(node.output)
		return operation.output

# Creating a function: f(z) = Ax + B
# Taking A = 10 and B = 1 for instance 

graph = Graph()
graph.set_as_default()
A = Variable(10)
b = Variable(1)
x = Placeholder()
y = mul(A, x)
z = add(y, b)
sess = Session()
sess.run(z, {x: 10}) 






