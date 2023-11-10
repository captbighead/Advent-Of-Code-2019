import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(24)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"....#", 
	"#..#.", 
	"#..##", 
	"..#..", 
	"#...."
]

class bug_cell:

	def __init__(self, infested, x, y, reg) -> None:
		self.xy = (x, y)
		self.x = x
		self.y = y
		self.infested = infested
		self.pending = None
		self.bio_potential = 2 ** (y * 5 + x)
		self.registry = reg

		self.neighbours = []
		for v in algos.unit_vectors():
			n = algos.vadd(self.xy, v)
			if n[0] in (-1, 5) or n[1] in (-1, 5):
				continue
			self.neighbours.append(n)

		reg[x, y] = self

	def prepare(self):
		nscore = sum(self.registry[n].infested for n in self.neighbours)
		if nscore != 1 and self.infested == 1:
			self.pending = 0
		elif nscore in (1, 2) and self.infested == 0:
			self.pending = 1
		else:
			self.pending = self.infested
	
	def apply(self):
		self.infested = self.pending
		self.pending = None
		return self.bio_potential * self.infested

class bug_cell_recursive:

	def __init__(self, infested, x, y, d, reg, first_prep=True) -> None:
		self.xyd = (x, y, d)
		self.x = x
		self.y = y
		self.d = d
		self.infested = infested
		self.first_prep = first_prep
		self.pending = None
		self.registry = reg

		self.neighbours = []
		for v in algos.unit_vectors():
			# Assume the best: that they're on the same level. 
			n = algos.vadd((x, y), v)
			nd = d					
			neighbours_to_add = [(n[0], n[1], nd)]

			# Then, check that assumption

			# If the x or y is out of bounds of the 5x5 grid, it reaches out to
			# another grid at d-1, from the (2, 2) position in that grid. 
			if n[0] in (-1, 5) or n[1] in (-1, 5):
				nx = 2 + (n[0] // abs(n[0]) if n[0] in (-1, 5) else 0)
				ny = 2 + (n[1] // abs(n[1]) if n[1] in (-1, 5) else 0)
				n = (nx, ny)
				nd = d - 1
				neighbours_to_add = [(nx, ny, nd)]

			# If n is (2, 2), we're not pointing at one cell, but 5 cells on the
			# edge of a deeper level. 
			elif n == (2, 2):
				nd = d + 1
				neighbours_to_add = []
				fixed_ind = 0 if v[0] != 0 else 1
				dynamic_i = 1 if not fixed_ind else 0
				for di in range(5):
					nxy_l = [-1, -1]
					nxy_l[fixed_ind] = 0 if v[fixed_ind] == 1 else 4
					nxy_l[dynamic_i] = di
					nxy_l.append(nd)
					neighbours_to_add.append(tuple(nxy_l))

			
			self.neighbours.extend(neighbours_to_add)

		reg[x, y, d] = self

	def prepare(self):
		# Slightly different scoring mechanism. 
		nscore = 0
		new_depth = 0
		for xyd in self.neighbours:
			n = self.registry.get(xyd, None)

			# Two cases exist where we're trying to access a neighbour of an as-
			# yet-unseen depth: We were created in this prep cycle, or we were
			# created in the last prep cycle. If we were created in this prep 
			# cycle, we can't be infested and can't infest further layers, so
			# there is no need to call for our unseen neighbours to be created.
			# (Doing so would cause an infinite loop, in fact!) So check if this
			# is our first prep cycle before remembering to demand our new layer
			# is created. 
			if n == None and not self.first_prep:
				new_depth = xyd[2]
				continue

			# If this is our first prep cycle in existence, then the fact that 
			# this unknown depth doesn't exist doesn't matter. It doesn't affect
			# us because it's empty, and we won't affect it until our next cycle
			# because at this point we're also empty. Therefore, we don't report
			# the new depth via our return value, and the nscore stays the same
			elif n == None and self.first_prep:
				continue
				
			else:
				nscore += n.infested
		
		# Now we interpret our neighbour score to see if we change. 
		if nscore != 1 and self.infested == 1:
			self.pending = 0
		elif nscore in (1, 2) and self.infested == 0:
			self.pending = 1
		else:
			self.pending = self.infested

		self.first_prep = False		# We have done a prep cycle now. 
		return new_depth	# Forward a request for a new layer for next time
		
	
	def apply(self):
		self.infested = self.pending
		self.pending = None


def do_part_one_for(lines):
	def display_game(game):
		# These lines allow us to view each iteration of the game to see what's
		# happening.
		map = {xy: "#" if game[xy].infested else " " for xy in game}
		algos.print_map(map)
		input()

	game = {}
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			bug_cell(1 if lines[y][x] == "#" else 0, x, y, game)

	# Comment out to automate
	#display_game(game)
	
	t = 0
	record = collections.defaultdict(list)
	record[sum([c.bio_potential * c.infested for c in game.values()])].append(0)
	while True:
		t += 1
		this_score = 0
		for xy in game.keys():
			game[xy].prepare()
		for xy in game.keys():
			this_score += game[xy].apply()

		# Comment out to automate
		#display_game(game)

		record[this_score].append(t)
		if len(record[this_score]) > 1:
			return this_score
		
def do_part_two_for(lines, iterations):
	game = {}
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			# These cells don't exist, ever.
			if (x, y) == (2, 2):
				continue

			infested = 1 if lines[y][x] == "#" else 0

			# First_Prep is false here because these have always existed
			bug_cell_recursive(infested, x, y, 0, game, False)
	
	for i in range(iterations):
		# Prep the existing generations that we already know about and see if 
		# they'll ask for new generations to create
		xyds_at_i = [xyd for xyd in game.keys()]
		new_depths_to_gen = set([])
		for xyd in xyds_at_i:
			new_depth_requested = game[xyd].prepare()
			if new_depth_requested:
				new_depths_to_gen.add(new_depth_requested)
		
		# Build the new generations we're affecting for the first time.
		new_generation = []
		for nd in new_depths_to_gen:
			for x in range(5):
				for y in range(5):
					# These cells don't exist, ever.
					if (x, y) == (2, 2):
						continue
					new_generation.append(bug_cell_recursive(0, x, y, nd, game))
		for bc in new_generation:
			bc.prepare()

		# This includes both the old guard and the new generation, whom have all
		# been prepped.
		for xyd in game.keys():
			game[xyd].apply()
	
	# Debugging for trouble shooting. 
	#if iterations < 11:
	#	d_min = min([xyd[2] for xyd in game.keys()])
	#	d_max = max([xyd[2] for xyd in game.keys()])
	#	for d in range(d_min, d_max+1):
	#		print(f"\tDEPTH: {d}")
	#		for y in range(5):
	#			print("\t\t", end="")
	#			for x in range(5):
	#				if (x, y) == (2, 2):
	#					print("?", end="")
	#					continue
	#				char = "#" if game[(x, y, d)].infested else " "
	#				print(f"{char}", end="")
	#			print()

	# Finally, count the existing bugs. 
	return sum(game[xyd].infested for xyd in game.keys())


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Simulate a version of Conway's Game of Life, and report the bitmap "
       	  f"of the first state that appears twice.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe 'biodiversity score' is {results}")
	print(f"\tWe expected: 2129920\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe 'biodiversity score' is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"The bugs now exist in infinitely recursive layers. Count the bugs a"
       	  f"fter 200 ticks.\n")

	results = do_part_two_for(example_lines, 10)
	print(f"When we do part two for the example input:")
	print(f"\tThe number of bugs is {results}")
	print(f"\tWe expected: 99\n")

	results = do_part_two_for(input_lines, 200)
	print(f"When we do part two for the actual input:")
	print(f"\tThe number of bugs is {results}\n")
