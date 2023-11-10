import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections
import heapq

try:
	input_lines = io.read_input_as_lines(18)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"########################", 
	"#@..............ac.GI.b#", 
	"###d#e#f################", 
	"###A#B#C################", 
	"###g#h#i################", 
	"########################", 
]

example_lines = [
	"#################",
	"#i.G..c...e..H.p#",
	"########.########",
	"#j.A..b...f..D.o#",
	"########@########",
	"#k.E..a...g..B.n#",
	"########.########",
	"#l.F..d...h..C.m#",
	"#################"
]

example_lines = [
	"########################",
	"#...............b.C.D.f#",
	"#.######################",
	"#.....@.a.B.c.d.A.e.F.g#",
	"########################"
]

example_lines_two = [
	"###############", 
	"#d.ABC.#.....a#", 
	"######...######", 
	"######.@.######", 
	"######...######", 
	"#b.....#.....c#", 
	"###############"
]

example_lines_two = [
	"#############",
	"#DcBa.#.GhKl#",
	"#.###...#I###",
	"#e#d#.@.#j#k#",
	"###C#...###J#",
	"#fEbA.#.FgHi#",
	"#############"
]

def dijkstra(space, orig, dest, impassible):
	Q_ENTRY = 0	# for heapq purposes
	visited = set([])
	unvisited = []
	def add_unvisited(path, xy):
		nonlocal Q_ENTRY
		heapq.heappush(unvisited, (len(path), Q_ENTRY, xy, path))
		Q_ENTRY += 1
	add_unvisited([], orig)
	path_map = collections.defaultdict(lambda: None)
	path_map[orig] = 0

	while len(unvisited):
		visit = heapq.heappop(unvisited)
		vxy = visit[2]
		vpath = visit[3]

		# If we've made it to the goal, then we're done. 
		if vxy == dest:
			return vpath

		# If we're visiting this node for the first time, do the visit. 
		# Otherwise, we were too slow to get here.
		if vxy in visited:
			continue
		else:
			visited.add(vxy)
		
		# Add the next potential visits. 
		for vec in algos.unit_vectors():
			nxy = algos.vadd(vec, vxy)
			if impassible(nxy) or nxy in visited:
				continue
			npath = vpath.copy()
			npath.append(nxy)
			add_unvisited(npath, nxy)
	
def parse_vault(lines):
	# The lookup to be returned. 
	path_lookup = {}

	# Create grid map of all nodes
	keys = []
	key_coords = {}
	grid = collections.defaultdict(lambda: "#")
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			grid[(x,y)] = lines[y][x]
			if grid[(x,y)].islower() or grid[(x,y)] == "@":
				keys.append(grid[(x,y)])
				key_coords[grid[(x, y)]]= (x, y)
	
	# An "is_impassible" function for dijkstra's to use.
	def is_wall(xy):
		return grid[xy] == "#" 
	
	# For each pair of keys that we need to path to/from, find the shortest path
	# and the required keys between them. 
	for i in range(len(keys)):
		for j in range(i+1, len(keys)):
			ki = keys[i]
			kj = keys[j]
			ij_path = dijkstra(grid, key_coords[ki], key_coords[kj], is_wall)
			ij_doors = [grid[cxy] for cxy in ij_path if grid[cxy].isupper()]
			ij_reqs = set([d.lower() for d in ij_doors])
			path_lookup[(ki, kj)] = (len(ij_path), ij_reqs)
			path_lookup[(kj, ki)] = (len(ij_path), ij_reqs)

	# path_lookup is a map of pairs of keys to pairs of the distance between 
	# them and the requisite keys you already need to have to get there.
	return path_lookup


def do_part_one_for(lines):
	path_lookup = parse_vault(lines)
	keys_unsorted = set([])
	for k in path_lookup.keys():
		keys_unsorted.add(k[0])
		keys_unsorted.add(k[1])
	
	# With the above algorithm, we now have the lengths it takes to get from any
	# node to any other node and the requisite keys needed to be able to do that
	#
	# Now if we use a priority queue and a modified dijkstra's algorithm, we can
	# find the shortest path to having all of the keys collected. 
	Q_ENTRY = 0	# Needed to use the heapq as a priority queue
	keys_sorted = sorted(keys_unsorted)

	# We can now track found keys in an int acting as a bitmap
	key_bit = {}
	for i in range(len(keys_sorted)):
		key_bit[keys_sorted[i]] = 2 ** i
	finished_mask = sum(key_bit.values())

	# Track if we've been to a set of nodes before.
	visited = {}

	# Implement our priority queue
	unvisited = []
	def add_unvisited(dist, path_str, visit_mask):
		nonlocal unvisited
		nonlocal Q_ENTRY
		heapq.heappush(unvisited, (dist, Q_ENTRY, path_str, visit_mask))
		Q_ENTRY += 1
	add_unvisited(0, "@", key_bit["@"])

	# Now we can dijkstra it up... 
	while len(unvisited):
		next_visit = heapq.heappop(unvisited)
		vdist = next_visit[0]
		vstr = next_visit[2]
		vmask = next_visit[3]

		# Check if by getting here we've been to all possible keys as fast as
		# possible
		if vmask == finished_mask:
			print(f"\tThe shortest path is: {vstr}")
			return vdist

		# Mark as visited or continue on if we have already visited
		if (vmask, vstr[-1]) in visited.keys():
			continue
		visited[(vmask, vstr[-1])] = vdist

		# Now we add all of our potential next paths.
		for k in keys_sorted:
			# If we've been to this key, continue on
			if key_bit[k] & vmask:
				continue

			# If we can't access this key, continue on
			accessible = True
			for req in path_lookup[(vstr[-1], k)][1]:
				accessible = accessible and key_bit[req] & vmask != 0
			if not accessible:
				continue

			# We *can* access k and we haven't done so before. Add it to the 
			# unvisited priority queue
			udist = path_lookup[(vstr[-1], k)][0]
			add_unvisited(vdist + udist, vstr + k, vmask + key_bit[k])

def parse_vault_part_two(lines):
	# We needed to change the logic for how the vault is parsed into the logic 
	# for how the vaultS are parsed, which is pretty minor.

	# The lookup to be returned. 
	path_lookup = {}

	# FIRST CHANGFE: Replace the center of the maze. 
	for y in range(len(lines)):
		breakout = False
		for x in range(len(lines[y])):
			if lines[y][x] == "@":
				lines[y-1] = lines[y-1][:x-1] + "1#2" + lines[y-1][x+2:]
				lines[y] = lines[y][:x-1] + "###" + lines[y][x+2:]
				lines[y+1] = lines[y+1][:x-1] + "3#4" + lines[y+1][x+2:]
				breakout = True
				break
		if breakout:
			break

	# Create grid map of all nodes
	keys = []
	key_coords = {}
	grid = collections.defaultdict(lambda: "#")
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			grid[(x,y)] = lines[y][x]
			if grid[(x,y)].islower() or grid[(x,y)].isnumeric():
				keys.append(grid[(x,y)])
				key_coords[grid[(x, y)]]= (x, y)
	
	# An "is_impassible" function for dijkstra's to use.
	def is_wall(xy):
		return grid[xy] == "#" 
	
	# For each pair of keys that we need to path to/from, find the shortest path
	# and the required keys between them. 
	for i in range(len(keys)):
		for j in range(i+1, len(keys)):
			ki = keys[i]
			kj = keys[j]
			ij_path = dijkstra(grid, key_coords[ki], key_coords[kj], is_wall)

			# LAST CHANGE: Be prepared for N/A paths to show up.  
			if ij_path == None:
				continue

			
			ij_doors = [grid[cxy] for cxy in ij_path if grid[cxy].isupper()]
			ij_reqs = set([d.lower() for d in ij_doors])
			path_lookup[(ki, kj)] = (len(ij_path), ij_reqs)
			path_lookup[(kj, ki)] = (len(ij_path), ij_reqs)

	# path_lookup is a map of pairs of keys to pairs of the distance between 
	# them and the requisite keys you already need to have to get there.
	return path_lookup

def do_part_two_for(lines):
	# Another copy-paste of part one, with implementation changes to make the 4
	# agents thing work. 
	path_lookup = parse_vault_part_two(lines)
	keys_unsorted = set([])
	for k in path_lookup.keys():
		keys_unsorted.add(k[0])
		keys_unsorted.add(k[1])

	# Now if we use a priority queue and a modified dijkstra's algorithm, we can
	# find the shortest path to having all of the keys collected. 
	Q_ENTRY = 0	# Needed to use the heapq as a priority queue
	keys_sorted = sorted(keys_unsorted)

	# We can now track found keys in an int acting as a bitmap
	key_bit = {}
	for i in range(len(keys_sorted)):
		key_bit[keys_sorted[i]] = 2 ** i
	finished_mask = sum(key_bit.values())

	# Track if we've been to a set of nodes before.
	visited = {}

	# Implement our priority queue
	unvisited = []
	def add_unvisited(dist, path_str, visit_mask):
		nonlocal unvisited
		nonlocal Q_ENTRY
		heapq.heappush(unvisited, (dist, Q_ENTRY, path_str, visit_mask))
		Q_ENTRY += 1
	origin_mask = sum([key_bit[o] for o in ["1", "2", "3", "4"]])
	add_unvisited(0, "1234", origin_mask)

	# Now we can dijkstra it up... 
	while len(unvisited):
		next_visit = heapq.heappop(unvisited)
		vdist = next_visit[0]
		vstr = next_visit[2]
		vmask = next_visit[3]

		# Check if by getting here we've been to all possible keys as fast as
		# possible
		if vmask == finished_mask:
			return vdist

		# Mark as visited or continue on if we have already visited
		if (vmask, vstr[-4:]) in visited.keys():
			continue
		visited[(vmask, vstr[-4:])] = vdist

		# Now we add all of our potential next paths.
		for k in keys_sorted:
			# If k is an agent, skip it
			if k.isnumeric():
				continue

			# If we've been to this key, continue on
			if key_bit[k] & vmask:
				continue

			# Now for each key we check we need to see if it's accessible to 
			# *its* agent.
			agent_path_str = vstr[-4:]
			agent_path_key = None
			for i in range(4):
				potential_agent_path_key = (agent_path_str[i], k)
				if potential_agent_path_key in path_lookup.keys():
					agent_path_key = potential_agent_path_key
					break

			# If we can't access this key, continue on
			accessible = True
			for req in path_lookup[agent_path_key][1]:
				accessible = accessible and key_bit[req] & vmask != 0
			if not accessible:
				continue

			# We *can* access k and we haven't done so before. Add it to the 
			# unvisited priority queue
			nstr = agent_path_str.replace(agent_path_key[0], k)
			udist = path_lookup[agent_path_key][0]
			add_unvisited(vdist + udist, vstr + nstr, vmask + key_bit[k])

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We are in an underground vault and need to collect a series of keys"
       	  f" in the fewest steps possible. Each key opens its corresponding doo"
		  f"r, so some keys are gated behind the retrieval of other keys.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe the least number of steps possible is {results}")
	#print(f"\tWe expected: 81\n")
	#print(f"\tWe expected: 136\n")
	print(f"\tWe expected: 132\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe the least number of steps possible is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we do the same thing, except our maze is distributed into four "
       	  f"sub-mazes, each with it's own agent.\n")

	results = do_part_two_for(example_lines_two)
	print(f"When we do part two for the example input:")
	print(f"\tThe minimum steps across four agents is {results}")
	print(f"\tWe expected: 32\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe minimum steps across four agents is {results}\n")
