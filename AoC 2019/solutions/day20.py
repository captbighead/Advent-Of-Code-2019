import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections
import heapq

try:
	input_lines = io.read_input_as_lines(20, strip=False)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"                   A               ", 
	"                   A               ", 
	"  #################.#############  ", 
	"  #.#...#...................#.#.#  ", 
	"  #.#.#.###.###.###.#########.#.#  ", 
	"  #.#.#.......#...#.....#.#.#...#  ", 
	"  #.#########.###.#####.#.#.###.#  ", 
	"  #.............#.#.....#.......#  ", 
	"  ###.###########.###.#####.#.#.#  ", 
	"  #.....#        A   C    #.#.#.#  ", 
	"  #######        S   P    #####.#  ", 
	"  #.#...#                 #......VT", 
	"  #.#.#.#                 #.#####  ", 
	"  #...#.#               YN....#.#  ", 
	"  #.###.#                 #####.#  ", 
	"DI....#.#                 #.....#  ", 
	"  #####.#                 #.###.#  ", 
	"ZZ......#               QG....#..AS", 
	"  ###.###                 #######  ", 
	"JO..#.#.#                 #.....#  ", 
	"  #.#.#.#                 ###.#.#  ", 
	"  #...#..DI             BU....#..LF", 
	"  #####.#                 #.#####  ", 
	"YN......#               VT..#....QG", 
	"  #.###.#                 #.###.#  ", 
	"  #.#...#                 #.....#  ", 
	"  ###.###    J L     J    #.#.###  ", 
	"  #.....#    O F     P    #.#...#  ", 
	"  #.###.#####.#.#####.#####.###.#  ", 
	"  #...#.#.#...#.....#.....#.#...#  ", 
	"  #.#####.###.###.#.#.#########.#  ", 
	"  #...#.#.....#...#.#.#.#.....#.#  ", 
	"  #.###.#####.###.###.#.#.#######  ", 
	"  #.#.........#...#.............#  ", 
	"  #########.###.###.#############  ", 
	"           B   J   C               ", 
	"           U   P   P               "
]

example_lines = [
	"         A           ",
	"         A           ",
	"  #######.#########  ",
	"  #######.........#  ",
	"  #######.#######.#  ",
	"  #######.#######.#  ",
	"  #######.#######.#  ",
	"  #####  B    ###.#  ",
	"BC...##  C    ###.#  ",
	"  ##.##       ###.#  ",
	"  ##...DE  F  ###.#  ",
	"  #####    G  ###.#  ",
	"  #########.#####.#  ",
	"DE..#######...###.#  ",
	"  #.#########.###.#  ",
	"FG..#########.....#  ",
	"  ###########.#####  ",
	"             Z       ",
	"             Z       "
]

example_lines_2 = [
	"             Z L X W       C                 ", 
	"             Z P Q B       K                 ", 
	"  ###########.#.#.#.#######.###############  ", 
	"  #...#.......#.#.......#.#.......#.#.#...#  ", 
	"  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ", 
	"  #.#...#.#.#...#.#.#...#...#...#.#.......#  ", 
	"  #.###.#######.###.###.#.###.###.#.#######  ", 
	"  #...#.......#.#...#...#.............#...#  ", 
	"  #.#########.#######.#.#######.#######.###  ", 
	"  #...#.#    F       R I       Z    #.#.#.#  ", 
	"  #.###.#    D       E C       H    #.#.#.#  ", 
	"  #.#...#                           #...#.#  ", 
	"  #.###.#                           #.###.#  ", 
	"  #.#....OA                       WB..#.#..ZH", 
	"  #.###.#                           #.#.#.#  ", 
	"CJ......#                           #.....#  ", 
	"  #######                           #######  ", 
	"  #.#....CK                         #......IC", 
	"  #.###.#                           #.###.#  ", 
	"  #.....#                           #...#.#  ", 
	"  ###.###                           #.#.#.#  ", 
	"XF....#.#                         RF..#.#.#  ", 
	"  #####.#                           #######  ", 
	"  #......CJ                       NM..#...#  ", 
	"  ###.#.#                           #.###.#  ", 
	"RE....#.#                           #......RF", 
	"  ###.###        X   X       L      #.#.#.#  ", 
	"  #.....#        F   Q       P      #.#.#.#  ", 
	"  ###.###########.###.#######.#########.###  ", 
	"  #.....#...#.....#.......#...#.....#.#...#  ", 
	"  #####.#.###.#######.#######.###.###.#.#.#  ", 
	"  #.......#.......#.#.#.#.#...#...#...#.#.#  ", 
	"  #####.###.#####.#.#.#.#.###.###.#.###.###  ", 
	"  #.......#.....#.#...#...............#...#  ", 
	"  #############.#.#.###.###################  ", 
	"               A O F   N                     ", 
	"               A A D   M                     "
]

class grid_space:
	def __init__(self, x, y, map, overrides) -> None:
		self.x = x
		self.y = y
		self.xy = (x, y)
		self.adjs = []

		# Find out which direction vector we need to override because of portals
		# (if any)
		override = overrides[self.xy]
		override_dir = override[0].upper() if override != None else None
		override_vec = override[1] if override != None else None

		# Figure out the space in each direction from our space. 
		labelled_vectors = algos.unit_vectors_labelled(True)
		for label in labelled_vectors.keys():
			vector = labelled_vectors[label]
			potential_adj = algos.vadd(vector, self.xy)
			
			# If we've overridden it this direction, use the override and move 
			# on
			if override_dir == label:
				self.adjs.append(override_vec)
				continue

			# Otherwise, add the space as adjacent iff it's navigable
			if map.get(potential_adj, "#") == ".":
				self.adjs.append(potential_adj)

class grid_space_part_two:

	def __init__(self, gsv1, outer_edge, inner_edge) -> None:
		self.xy = gsv1.xy
		self.x = gsv1.x
		self.y = gsv1.y

		if self.xy == (13, 8):
			print()

		self.inner = inner_edge(self.xy)
		self.outer = outer_edge(self.xy)
		const_adjs = [algos.vadd(self.xy, v) for v in algos.unit_vectors()]
		self.const_adjs = [ca for ca in gsv1.adjs if ca in const_adjs]
		self.contextual_adjs = [ca for ca in gsv1.adjs if ca not in const_adjs]

	def adjs(self, depth):
		# Constant adjacencies are independent of depth, and maintain their 
		# current depth
		if len(self.contextual_adjs) == 0:
			return [(adj, depth) for adj in self.const_adjs]
		
		# Adjacent spaces reached through portals change your depth, but outer
		# portals don't exist at depth 0.
		relevant_adjs = [(adj, depth) for adj in self.const_adjs.copy()]
		for ca in self.contextual_adjs:
			if self.outer and depth:
				relevant_adjs.append((ca, depth-1))
			elif self.inner: 
				relevant_adjs.append((ca, depth+1))
		return relevant_adjs


def parse_maze(lines):
	adj_overrides = collections.defaultdict(lambda: None)
	pending_overrides = {}
	skips = set([])
	map = collections.defaultdict(lambda:"#")
	orig = None
	dest = None
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			c = lines[y][x]

			# Skip empty spaces and label characters we've already processed
			if c == " " or (x, y) in skips:
				continue

			# If c is an upper-case character then it's part of some label. We 
			# scan from left to right, top to bottom, so the second character in
			# the label is either below this one or to the right. 
			if c.isupper():
				# Determine which way the label is oriented by finding the chars
				# below and to the right. Whichever one is also an upper-case 
				# character, that's the second char in the label. 
				below = lines[y+1][x] if y < len(lines) else "!"
				right = lines[y][x+1] if x < len(lines[y]) else "!"
				c2 = below if below.isupper() else right

				# Remember the space of the second character so we don't try to
				# re-process it as the start of a label later. 
				skips.add((x+1, y) if right.isupper() else (x, y+1))
				
				# Now we have the label, we can use it to track our weird 
				# spatial anomalies.
				label = c + c2
				labelled_space = None
				overridden_dir = None

				# Now we figure out the space that is labelled by our label. If
				# the space is a portal, then if they move from that space 
				# towards where the label is situated, they will end up going 
				# through the portal, so if the space that is labelled is above
				# the label, then adj space we need to override is down from the
				# labelled space. Repeat for all 4 orientations.
				#
				# below.isupper() indicates a vertical label. Since we work from
				# the top left to the bottom right, we have either seen the 
				# space above this label, or it's out of bounds. Either way, our
				# map (implemented as a defaultdict) will spit out a "." iff the
				# label is below the space. Otherwise, if below.isupper(), then
				# we know the labelled space is the one below our label. Repeat
				# for the left-right axis.
				if below.isupper() and map[x, y-1] == ".":	
					labelled_space = (x, y-1)
					overridden_dir = "d"
				elif below.isupper():
					labelled_space = (x, y+2)
					overridden_dir = "u"
				elif right.isupper() and map[x-1, y] == ".":
					labelled_space = (x-1, y)
					overridden_dir = "r"
				elif right.isupper():
					labelled_space = (x+2, y)
					overridden_dir = "l"

				# Now, the labelled space may not be a portal at all. If the 
				# label is AA or ZZ then it's just denoting the start/end of the
				# maze, respectively. 
				if label == "AA":
					orig = labelled_space
					continue	# Don't plot spaces in labels
				elif label == "ZZ":
					dest = labelled_space
					continue	# Don't plot spaces in labels

				# Lastly, we need to form the override. If this is the first 
				# instance of the portal label, then we can't finish logging the
				# override until we find the next one. 
				if pending_overrides.get(label, None) == None:
					pending_overrides[label] = (labelled_space, overridden_dir)
					continue	# Don't plot spaces in labels

				# If this *isn't* the first time we've seen this portal label, 
				# we can set up both endpoints' overrides: 
				other = pending_overrides.pop(label)
				adj_overrides[other[0]] = (other[1], labelled_space)
				adj_overrides[labelled_space] = (overridden_dir, other[0])
				continue	# Don't plot spaces in labels

			# If it wasn't a blank space or a label, we get here, and plot it
			map[x,y] = lines[y][x]

	final_mapping = {}
	for xy in map.keys():
		gs = grid_space(xy[0], xy[1], map, adj_overrides)
		final_mapping[xy] = gs
	return (final_mapping, orig, dest)

def pri_queue_dijkstra(grid, orig, dest):
	# Initialize data structures
	ENTRY_INDEX = 0		# Needed to make heapq work as priority queue
	visited = set([])
	unvisited = []
	def add_unvisited(coord, cost):	# Encapsulate the ENTRY_INDEX nonsense
		nonlocal ENTRY_INDEX
		heapq.heappush(unvisited, (cost, ENTRY_INDEX, coord))
		ENTRY_INDEX += 1
	add_unvisited(orig, 0)

	# Actual dijkstra algorithm
	while len(unvisited):
		visit_data = heapq.heappop(unvisited)
		visit_xy = visit_data[2]
		visit_cost = visit_data[0]

		# If we're done we're done.
		if visit_xy == dest:
			return visit_cost

		# Confirm if we've already been here or not and handle it appropriately
		if visit_xy in visited:
			continue
		else:
			visited.add(visit_xy)

		# If we get here, we need to add any adjacent nodes we haven't been to
		# before to our unvisited queue
		for adj in grid[visit_xy].adjs:
			if adj in visited:
				continue
			else:
				add_unvisited(adj, visit_cost + 1)


def pri_queue_dijkstra_two(grid, orig, dest):
	# Initialize data structures
	ENTRY_INDEX = 0		# Needed to make heapq work as priority queue
	visited = set([])
	unvisited = []
	def add_unvisited(coord, depth, cost):	# Encapsulate ENTRY_INDEX nonsense
		nonlocal ENTRY_INDEX
		heapq.heappush(unvisited, (cost, ENTRY_INDEX, coord, depth))
		ENTRY_INDEX += 1
	add_unvisited(orig, 0, 0)

	# Actual dijkstra algorithm
	while len(unvisited):
		visit_data = heapq.heappop(unvisited)
		visit_xy = visit_data[2]
		visit_depth = visit_data[3]
		visit_cost = visit_data[0]

		# If we're done we're done.
		if visit_xy == dest and not visit_depth:
			return visit_cost

		# Confirm if we've already been here or not and handle it appropriately
		if (visit_xy, visit_depth) in visited:
			continue
		else:
			visited.add((visit_xy, visit_depth))

		# If we get here, we need to add any adjacent nodes we haven't been to
		# before to our unvisited queue
		for adj_d in grid[visit_xy].adjs(visit_depth):
			adj = adj_d[0]
			d = adj_d[1]
			if adj_d in visited:
				continue
			else:
				add_unvisited(adj, d, visit_cost + 1)

def adjust_map_for_part_two(orig_map, input_width, input_height):
	# We already have a really good working map and data structure, we just need
	# to embed within it the logic for moving between depths. To do that, we 
	# need to identify the inner and outer rings of the map.
	X_OUTER = (2, input_width-3)
	Y_OUTER = (2, input_height-3)
	def outer_edge(xy):
		tb = xy[0] >= X_OUTER[0] and xy[0] <= X_OUTER[1] and xy[1] in Y_OUTER
		lr = xy[1] >= Y_OUTER[0] and xy[1] <= Y_OUTER[1] and xy[0] in X_OUTER
		return tb or lr
	
	top_left_inner = False
	for y in range(Y_OUTER[0], Y_OUTER[1]+1):
		for x in range(X_OUTER[0], X_OUTER[1]+1):
			top_left_inner = orig_map.get((x, y), None) == None
			if top_left_inner:
				top_left_inner = (x-1, y-1)
				break
		if top_left_inner:
			break
	bottom_right_inner = False
	for y in range(Y_OUTER[1], Y_OUTER[0]-1, -1):
		for x in range(X_OUTER[1], X_OUTER[0]-1, -1):
			bottom_right_inner = orig_map.get((x, y), None) == None
			if bottom_right_inner:
				bottom_right_inner = (x+1, y+1)
				break
		if bottom_right_inner:
			break
	X_INNER = (top_left_inner[0], bottom_right_inner[0])
	Y_INNER = (top_left_inner[1], bottom_right_inner[1])
	def inner_edge(xy):
		tb = xy[0] >= X_INNER[0] and xy[0] <= X_INNER[1] and xy[1] in Y_INNER
		lr = xy[1] >= Y_INNER[0] and xy[1] <= Y_INNER[1] and xy[0] in X_INNER
		return tb or lr

	# Now we can tell if a position is on an inner edge or an outer edge. From 
	# here, we can now make a new grid_space that provides its adjacent spaces 
	# based on a parameter, and also pairs them with a delta_depth for if they
	# change the recursive depth. 
	retmap = {}
	for xy in orig_map.keys():
		retmap[xy] = grid_space_part_two(orig_map[xy], outer_edge, inner_edge)
	return retmap

def do_part_one_for(lines):
	map = parse_maze(lines)
	return pri_queue_dijkstra(map[0], map[1], map[2])

def do_part_two_for(lines):
	map_package = parse_maze(lines)
	map = map_package[0]
	orig = map_package[1]
	dest = map_package[2]
	map = adjust_map_for_part_two(map, len(lines[0]), len(lines))
	return pri_queue_dijkstra_two(map, orig, dest)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We've been given a maze with portals. What's the fastest route thro"
       	  f"ugh the maze?\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe fastest route through the maze takes {results} steps")
	#print(f"\tWe expected: 58\n")
	print(f"\tWe expected: 23\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe fastest route through the maze takes {results} steps\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Okay this one's fascinating. Now, when we take a portal on an inner"
       	  f" wall, we are actually teleporting into a mirror-dimension version "
		  f"of the maze, and if we step through a portal on an outer wall, we a"
		  f"re teleporting out to a higher level dimension.\n")

	results = do_part_two_for(example_lines_2)
	#results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe  fastest route through the interdimensional, recursive maze i"
		  f"s {results}")
	print(f"\tWe expected: 396\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe  fastest route through the interdimensional, recursive maze i"
		  f"s {results}\n")
