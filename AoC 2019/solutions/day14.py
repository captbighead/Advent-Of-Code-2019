import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(14)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"10 ORE => 10 A", 
	"1 ORE => 1 B", 
	"7 A, 1 B => 1 C", 
	"7 A, 1 C => 1 D", 
	"7 A, 1 D => 1 E", 
	"7 A, 1 E => 1 FUEL"
]

example_lines = [
	"157 ORE => 5 NZVS", 
	"165 ORE => 6 DCFZ", 
	"44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL", 
	"12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", 
	"179 ORE => 7 PSHF", 
	"177 ORE => 5 HKGWZ", 
	"7 DCFZ, 7 PSHF => 2 XJWVT", 
	"165 ORE => 2 GPVTF", 
	"3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
]

class chemnode:

	def __init__(self, recipe, registry) -> None:
		self.registry = registry
		self.name = recipe.split(" => ")[1].split(" ")[1]
		self.quantity = int(recipe.split(" => ")[1].split(" ")[0])
		self.reqs = [tok for tok in recipe.split(" => ")[0].split(", ")]
		self.reqs = {t.split(" ")[1]: int(t.split(" ")[0]) for t in self.reqs}
		self.registry[self.name] = self

	def resolve_cost(self, quota_copy, surplus):
		# Find out how many batches of our material we need to make
		# Use up the surplus first:
		quota = quota_copy
		in_surplus = surplus[self.name]
		if in_surplus >= quota:
			surplus[self.name] -= quota
			return 0
		
		# If we get here, we have less surplus than we need to resolve this
		quota -= in_surplus
		surplus[self.name] = 0

		# Now we figure out how many batches of the recipe we need to make to 
		# get our material.
		#batches = 1
		#while (batches * self.quantity) < quota:
		#	batches += 1
		batches = quota // self.quantity + (1 if quota % self.quantity else 0)
		
		# batches * self.quantity = 

		# Knowing how many batches we need to make, we need to find the cost of
		# the ingredients used in that many batches. 
		cost = 0
		for ing in self.reqs.keys():
			ing_quota = batches * self.reqs[ing]
			if ing == "ORE":
				cost += ing_quota
			else:
				cost += self.registry[ing].resolve_cost(ing_quota, surplus)

		# Lastly, track how much surplus is made
		surplus[self.name] += batches * self.quantity - quota 

		return cost

	

def do_part_one_for(lines):
	registry = {}
	for ln in lines:
		chemnode(ln, registry)
	return registry["FUEL"].resolve_cost(1, collections.defaultdict(int))

def do_part_two_for(lines):
	registry = {}
	for ln in lines:
		chemnode(ln, registry)
	node = registry["FUEL"]

	# shorthand, generates a new storage for the surplus. Needs a blank storage
	# for each calculation
	def surplus():
		return collections.defaultdict(int)

	# Search the space, using smaller and smaller jumps until you find it to the
	# ones place. 
	ONETRILLION = 1000000000000
	exp = 11
	guess = 0
	while exp >= 0:
		while node.resolve_cost(guess + (10 ** exp), surplus()) < ONETRILLION:
			guess += 10 ** exp

		# Cost at next guest would be above one trillion, make a smaller guess.
		exp -= 1

	return guess

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We are given a list of chemical reactions and asked to find out how"
       	  f" much ORE is needed to create one unit of FUEL.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe required number of units of ORE is {results}")
	#print(f"\tWe expected: 31\n")
	print(f"\tWe expected: 13312\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe required number of units of ORE is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe fuel producable by 1 trillion ore is {results}")
	print(f"\tWe expected: 82892753 \n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe fuel producable by 1 trillion ore is {results}\n")
