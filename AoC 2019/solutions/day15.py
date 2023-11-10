import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(15)
except:
	input_lines = ["Input Lines Not Found"]
	pass

PART_1_MAP = None

DIRS = {1:(0, -1), 2:(0, 1), 3:(-1, 0), 4:(1, 0)}
DIR_INPUTS = {DIRS[xy]: xy for xy in DIRS.keys()}
OPPS = {1:2, 2:1, 3:4, 4:3}
UNKNOWN = -1
EMPTY = 1
WALL = 0
OXY = 2

class smarter_robot:

	def __init__(self, program) -> None:
		self.brain = ic.intcode_computer(program)
		self.xy = (0, 0)
		self.unsearched = collections.deque([(0,0)])
		self.map = collections.defaultdict(lambda:UNKNOWN)
		self.map[self.xy] = EMPTY

	def cartograph(self):
		while len(self.unsearched):
			# Find the next unsearched space and navigate to it directly. 
			next = self.unsearched.popleft()
			is_goal = lambda xy: xy == next
			is_impassible = lambda xy: self.map[xy] in (UNKNOWN, WALL)
			path = algos.dijkstra(self.map, is_goal, is_impassible, self.xy)
			while len(path):
				step = path.popleft()
				self.xy = algos.vadd(self.xy, step)
				self.brain.qinp.append(DIR_INPUTS[step])
				self.brain.run()
				self.brain.qout.popleft()

			# Use the same search protocol the dumb robot used:
			for d in DIRS.keys():
				# Record details about what we're about to try
				undo = OPPS[d]
				coord = algos.vadd(self.xy, DIRS[d])

				# If we've already seen the space in that direction, skip
				if self.map[coord] != UNKNOWN:
					continue

				# Trial it. 
				self.brain.qinp.append(d)
				self.brain.run()
				result = self.brain.qout.popleft()

				if result == WALL:
					self.map[coord] = WALL
					continue
				else:
					self.map[coord] = result
					self.unsearched.append(coord)
					self.brain.qinp.append(undo)
					self.brain.run()
					self.brain.qout.popleft()

		return self.map
					


class robot:

	def __init__(self, program) -> None:
		self.brain = ic.intcode_computer(program)
		self.way_home = collections.deque([])
		self.xy = (0, 0)
		self.objectives = collections.deque([collections.deque([])])
		self.map = collections.defaultdict(lambda:UNKNOWN)
		self.map[self.xy] = EMPTY

	def seek_objectives(self):
		while len(self.objectives):
			# Find the path from home to the next space to search. 
			objective = self.objectives.popleft()

			# Go to the next space via home.
			self.go_home()
			while len(objective):
				self.move(objective.popleft())
			
			# Search all 4 directions from the current space.
			for d in DIRS.keys():
				# Record details about what we're about to try
				undo = OPPS[d]
				coord = algos.vadd(self.xy, DIRS[d])

				# If we've already seen the space in that direction, skip
				if self.map[coord] != UNKNOWN:
					continue

				# Trial it. 
				result = self.move(d, False)

				if result == WALL:
					self.map[coord] = WALL
					continue
				else:	# EMPTY or OXY, we need to scope out that space later.
					new_path = self.way_home.copy()
					new_path.append(d)
					self.objectives.append(new_path)
					self.map[coord] = result
					self.move(undo, False)

		# We've mapped the entire space. Now we can find the shortest path
		return self.map

	def move(self, dir, log=True):
		potential_coord = algos.vadd(self.xy, DIRS[dir])
		self.brain.qinp.append(dir)
		self.brain.run()
		result = self.brain.qout.popleft()
		if result != 0:
			self.xy = potential_coord
		if log:
			self.way_home.append(dir)
		return result
	
	def go_home(self):
		while(len(self.way_home)):
			self.move(OPPS[self.way_home.pop()], False)

def do_part_one_for(lines):
	droid = smarter_robot(lines[0])
	world_map = droid.cartograph()
	global PART_1_MAP
	PART_1_MAP = world_map
	def is_goal(xy):
		return world_map[xy] == OXY
	def is_impassible(xy):
		return world_map[xy] == WALL
	return len(algos.dijkstra(world_map, is_goal, is_impassible))

def successful_but_slow__do_part_one_for(lines):
	droid = robot(lines[0])
	world_map = droid.seek_objectives()
	global PART_1_MAP
	PART_1_MAP = world_map
	def is_goal(xy):
		return world_map[xy] == OXY
	def is_impassible(xy):
		return world_map[xy] == WALL
	return len(algos.dijkstra(world_map, is_goal, is_impassible))
	
def do_part_two_for(lines):
	void_spaces = set([xy for xy in PART_1_MAP if PART_1_MAP[xy] == EMPTY])
	o2q = collections.deque([xy for xy in PART_1_MAP if PART_1_MAP[xy] == OXY])
	t = 0
	while len(void_spaces):
		next_min = collections.deque([])
		while len(o2q):
			spreader = o2q.popleft()
			for d in DIRS.keys():
				spc = algos.vadd(spreader, DIRS[d])
				if spc in void_spaces:
					void_spaces.remove(spc)
					next_min.append(spc)
		o2q = next_min
		t += 1
	return t



def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We need to find the ship's oxygen system using an intcode robot.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe shortest path to the oxygen system takes {results} steps\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe time to fill the ship with oxygen is {results}\n")
