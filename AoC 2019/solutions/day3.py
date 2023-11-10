import utilities.io as io
import utilities.algos as algos
import collections

try:
	input_lines = io.read_input_as_lines(3)
except:
	input_lines = [
		"R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
	]

example_lines = [
	"R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
	"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
]

def do_part_one_for(lines):
	gridmap = collections.defaultdict(set)
	dir_lookup = algos.unit_vectors_labelled()
	wire = 0
	for dirs in lines:
		cursor = (0,0)
		for dir in dirs.split(","):
			d = dir[0]
			i = int(dir[1:])
			for step in range(i):
				cursor = algos.vadd(cursor, dir_lookup[d])
				gridmap[cursor].add(wire)
		wire += 1
	best_dist = 999999999
	for xy in gridmap.keys():
		if len(gridmap[xy]) >= 2:
			best_dist = min(algos.distance_manhattan(xy, (0,0)), best_dist)
	return best_dist


def do_part_two_for(lines):
	gridmap = collections.defaultdict(dict)
	dir_lookup = algos.unit_vectors_labelled()
	wire = 0
	for dirs in lines:
		cursor = (0,0)
		steps = 0
		for dir in dirs.split(","):
			d = dir[0]
			i = int(dir[1:])
			for step in range(i):
				steps += 1
				cursor = algos.vadd(cursor, dir_lookup[d])
				if gridmap[cursor].get(wire, -1) == -1:
					gridmap[cursor][wire] = steps 
		wire += 1
	best_dist = 999999999
	for xy in gridmap.keys():
		if len(gridmap[xy].keys()) >= 2:
			best_dist = min(gridmap[xy][0] + gridmap[xy][1], best_dist)
	return best_dist

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"There are co-ordinates for two wires and we need to provide the Man"
       	  f"hattan Distance to the closest overlapping point to the origin of t"
		  f"he wires.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe distance to the closest overlap is {results}")
	print(f"\tWe expected: 135\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe distance to the closest overlap is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Same thing, but this time we're summing the minimum lengths of the "
       	  f"two wires at the closest overlap.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe signal delay is {results}")
	print(f"\tWe expected: 410\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe signal delay is {results}\n")
