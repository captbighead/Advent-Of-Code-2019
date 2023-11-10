import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

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

	# OKAY. Now we have a documented list of paths to get to all the places we 
	# need to, and requisite keys to get there. NOW we can BFS all the possible
	# routes to find the fastest one. 

	all_keys = set([k for k in path_tree.keys() if k != "@"])
	remaining_str = "".join(sorted(all_keys))
	bests = collections.defaultdict(lambda:999999999)
	search_space = collections.deque([(("@", 0, remaining_str))])
	while len(search_space):
		search_node = search_space.popleft()
		curr_k = search_node[0]
		curr_t = search_node[1]
		curr_remaining = search_node[2]
		
		# If we got to this set of remaining nodes faster in the past, then we 
		# don't need to entertain this node.
		if bests[(curr_k, curr_remaining)] < curr_t:
			continue

		# Otherwise, keep searching. 
		bests[(curr_k, curr_remaining)] = curr_t
		for next_k in curr_remaining:
			path_info = path_lookup[(curr_k, next_k)]
			path_dist = path_info[0]
			path_reqs = path_info[1]

			# Find the hypothetical next node. If it's been seen before at a 
			# faster speed than we could get to it, then there's no need to see
			# if it meets requirements. 
			next_remaining = curr_remaining.replace(next_k, "")
			next_t = curr_t + path_dist
			if next_t >= bests[(next_k, next_remaining)]:
				continue

			# Check requirements before adding this route to the search space
			# If we already have a path for this search state, we don't need to
			# check reqs *again*
			if bests[(next_k, next_remaining)] == 999999999:
				meets_reqs = True	# Can meet reqs until proven false
				for r in path_reqs:
					meets_reqs = meets_reqs and r not in curr_remaining
				if not meets_reqs:
					continue

			search_space.append((next_k, next_t, next_remaining))
	
	# Having searched all sequences we could acquire keys in, we now know all 
	# the best ways to get all keys:
	bests = {k:bests[k] for k in bests.keys() if k[1] == ""}
	return min(bests.values())

		

	



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
	print(f"\tWe expected: 81\n")

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
