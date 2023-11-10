import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(6)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU",
	"I)SAN"
]

class orbit_tree_node:

	def __init__(self, name) -> None:
		self.name = name
		self.parent = None
		self.children = []

	def orbits(self):
		return len(self.children) + sum([c.orbits() for c in self.children])

class search_node:
	
	def __init__(self, current_body) -> None:
		self.history = [current_body]
		self.current = current_body
	
	def possibilities(self):
		potentials = self.current.children.copy()
		if self.current.parent != None:
			potentials.append(self.current.parent)
		i = 0
		while i < len(potentials):
			if potentials[i] in self.history:
				potentials.pop(i)
				continue
			i += 1

		possibiles = []
		for p in potentials:
			poss = search_node(p)
			poss.history.extend(self.history)
			possibiles.append(poss)
		return possibiles


def generate_orbital_map(lines):
	all_bodies = {}
	for ln in lines:
		bodies = ln.split(")")
		pname = bodies[0]
		cname = bodies[1]
		parent = all_bodies.setdefault(pname, orbit_tree_node(pname))
		child = all_bodies.setdefault(cname, orbit_tree_node(cname))
		child.parent = parent
		parent.children.append(child)
	return all_bodies

def do_part_one_for(lines):
	all_bodies = generate_orbital_map(lines)
	return sum([body.orbits() for body in all_bodies.values()])

def do_part_two_for(lines):
	all_bodies = generate_orbital_map(lines)
	dest = all_bodies["SAN"].parent.name
	search_space = collections.deque([search_node(all_bodies["YOU"].parent)])

	while len(search_space):
		next = search_space.popleft()
		if next.current.name == dest:
			return len(next.history) - 1
		for p in next.possibilities():
			search_space.append(p)
	raise ValueError("The erroneous value is my logic.")
	
	
	

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We are given a map of orbital bodies and need to generate a tree fo"
       	  f"r them to be able to determine how many direct/indirect orbits each"
		  f" body has. Given the list, output the sum total of all orbits.\n")

	results = do_part_one_for(example_lines[:-2])
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of all direct and indirect orbits is {results}")
	print(f"\tWe expected: 42\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of all direct and indirect orbits is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now that we can calculate orbits, we need to be able to find the pa"
       	  f"th from the object we're ordering to the object that Santa is orbit"
		  f"ing.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of orbital transfers required is {results}")
	print(f"\tWe expected: 4\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of orbital transfers required is {results}\n")
