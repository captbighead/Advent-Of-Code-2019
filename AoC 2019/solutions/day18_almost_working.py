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

class path_node:

	def __init__(self, x, y, char, parent) -> None:
		self.x = x
		self.y = y
		self.char = char
		self.parent = parent
		self.children = []
	
	def adjacents(self):
		adjs = self.children.copy()
		if self.parent != None:
			adjs.append(self.parent)
		return adjs

def parse_vault(lines):
	# First, map it all out like normal. 
	vault = collections.defaultdict(lambda:"#")
	pois = {}
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			c = lines[y][x]
			vault[(x, y)] = c
			if c.isupper() or c.islower() or c == "@":
				pois[c] = (x, y)
	
	# Now, starting from "@", map out all paths from "@" as a tree. (ASSUMPTION:
	# there are no cycles in this graph and it is a tree.)
	o_xy = pois["@"]
	orig = path_node(o_xy[0], o_xy[1], "@", None)
	poi_path_nodes = {"@":orig}
	tree_construct_q = collections.deque([orig])
	visited = set([])
	while len(tree_construct_q):
		last = tree_construct_q.popleft()
		visited.add((last.x, last.y))
		for d in algos.unit_vectors():
			next_x = last.x + d[0]
			next_y = last.y + d[1]

			# Don't recreate nodes, and don't add walls as nodes. 
			if vault[(next_x, next_y)] == "#" or (next_x, next_y) in visited:
				continue

			next_c = vault[(next_x, next_y)]
			child = path_node(next_x, next_y, next_c, last)
			last.children.append(child)
			tree_construct_q.append(child)

			if next_c in pois.keys() and next_c.islower():
				poi_path_nodes[next_c] = child
	
	return poi_path_nodes


def do_part_one_for(lines):
	path_tree = parse_vault(lines)
	path_lookup = {}
	for n in path_tree.keys():
		orig = path_tree[n]
		visited = set([])
		# Queue tuples: node, dist, req_keys. Every pop adds 1 to distance, so 
		# the first pop (tracking from orig to orig) should be -1 so that when
		# the first add happens, it becomes 0. 
		queue = collections.deque([(orig, -1, set([]))])
		while len(queue):
			visit = queue.popleft()
			if (visit[0].x, visit[0].y) in visited:
				continue

			node = visit[0]
			dist = visit[1] + 1
			req_keys = visit[2].copy()
			visited.add((node.x, node.y))

			# Check this node for bookkeeping needs:
			
			# If this is a door that needs a key, add the key to its key set
			if node.char.isupper():
				req_keys.add(node.char.lower())

			# If this is a key, log the distance to it from orig, and the 
			# required keys to get to it.
			if node.char.islower() and node.char != orig.char:
				path_lookup[(orig.char, node.char)] = (dist, req_keys)

				if orig.char != "@":	# Don't plot a path back to spawn
					path_lookup[(node.char, orig.char)] = (dist, req_keys)

			for a in node.adjacents():
				if (a.x, a.y) in visited:	# Skip the one we used to get here
					continue
				queue.append((a, dist, req_keys))


	# With the above algorithm, we now have the lengths it takes to get from any
	# node to any other node and the requisite keys needed to be able to do that
	#
	# Now if we use a priority queue and a modified dijkstra's algorithm, we can
	# find the shortest path to having all of the keys collected. 
	Q_ENTRY = 0	# Needed to use the heapq as a priority queue
	keys_sorted = sorted(path_tree.keys())

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
	should_have_revisited = 0
	good_thing_we_didnt = 0
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


def do_part_two_for(lines):
	pass

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
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: <SOLUTION THEY WANT>\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
