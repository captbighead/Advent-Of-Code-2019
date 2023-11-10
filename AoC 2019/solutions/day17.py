import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(17)
except:
	input_lines = ["Input Lines Not Found"]
	pass

SCAFFOLD_MAP = None
ROBOT_START = None
SCAFFOLD = 1
ROBOT = 2
EMPTY = 0

def do_part_one_for(lines):
	ic_ascii = ic.intcode_computer(lines[0])
	ic_ascii.run()
	x = 0
	y = 0
	scaffold_map = collections.defaultdict(int)
	global ROBOT_START
	while ic_ascii.output_pending():
		next = ic_ascii.output()
		
		# If it's a newline character, reset x and increase y
		if next == 10:
			y += 1
			x = 0
			continue

		# Even if the input is a robot, the point being observed is scaffolding
		if next != 46:
			scaffold_map[(x, y)] = SCAFFOLD
			if ROBOT_START == None and next != 35:
				global ROBOT
				ROBOT = next
				ROBOT_START = (x, y)

		
		# Whether it's open space or scaffolding, x increments
		x += 1
	
	# Now that we have a picture of the scaffolding, iterate over the different
	# chunks. If they're surrounded by scaffolding, they're an intersection.
	sum_align_params = 0
	for xy in scaffold_map.copy().keys():
		adj_scaffs = 0
		for v in algos.unit_vectors():
			adj_scaffs += scaffold_map[algos.vadd(xy, v)]
		if adj_scaffs == 4:
			sum_align_params += xy[0] * xy[1]

	# Lastly, no need to reinvent the wheel. Pass on the scaffold map we made.
	global SCAFFOLD_MAP
	SCAFFOLD_MAP = scaffold_map
	return sum_align_params

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We're about to lose a bunch of robots to EMF, and need to control a"
       	  f" vacuum robot to pick up all the lil guys. First, we need to test t"
		  f"hat the camera is working but outputting the sum of all of the alig"
		  f"nment parameters for all of the intersections in the scaffolding.\n"
		  )

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we need to program the robot to navigate the scaffolding. Here'"
       	  f"s what the space looks like:\n")
	
	global SCAFFOLD_MAP
	SCAFFOLD_MAP[ROBOT_START] = ROBOT
	
	# Up and down are inverted relative to the unit_vectors function in algos, 
	# so we need to transpose the map.
	inverted = SCAFFOLD_MAP.copy()
	SCAFFOLD_MAP = collections.defaultdict(int)
	y_max = max([xy[1] for xy in inverted.keys()])
	for xy in inverted.keys():
		SCAFFOLD_MAP[(xy[0], y_max - xy[1])] = inverted[xy]

	# Print the map to keep the user in the loop for building the program.
	def renderer(n):
		if n == EMPTY:
			return " "
		elif n == SCAFFOLD:
			return "#"
		elif n == ROBOT:
			return chr(ROBOT)
	algos.print_map(SCAFFOLD_MAP, renderer, PRINT_BOUND=100)

	# The robot is oriented upwards, so the first step it has to take is to 
	# turn left (or to turn right 3 times, I guess...)

	# Create a quick and dirty crawler function to map out the moves the robot
	# needs to have programmed for it.
	dirs = algos.unit_vectors()
	xy = (ROBOT_START[0], y_max - ROBOT_START[1])
	dir = 0
	def next_move():
		nonlocal xy, dir
		front = SCAFFOLD_MAP[algos.vadd(xy, dirs[dir])]
		left =  SCAFFOLD_MAP[algos.vadd(xy, dirs[(dir-1)%4])]
		right = SCAFFOLD_MAP[algos.vadd(xy, dirs[(dir+1)%4])]
		fxy = algos.vadd(xy, dirs[dir])
		lxy = algos.vadd(xy, dirs[(dir-1)%4])
		rxy = algos.vadd(xy, dirs[(dir+1)%4])
		if front != EMPTY:
			xy = algos.vadd(xy, dirs[dir])
			return "F"	# First pass will be step-wise, then a second aggregates
		if left != EMPTY:
			dir = (dir - 1) % 4
			return "L"
		if right != EMPTY:
			dir = (dir + 1) % 4
			return "R"
		return None
	
	# ...Extract said moves. 
	stepwise_moves = [next_move()]
	while stepwise_moves[-1] != None:
		stepwise_moves.append(next_move())
	moves = []
	for i in stepwise_moves:
		if i == "F" and isinstance(moves[-1], int):
			moves[-1] += 1
		elif i == "F":
			moves.append(1)
		elif i != None:
			moves.append(i)
	
	print(f"The full sequence of moves that need to be made by the robot (and t"
       	  f"hus, programmed into three subroutines) is as follows:\n")
	print("\t",end="")
	last_three = []
	for m in moves:
		if len(last_three) < 3:
			last_three.append(m)
		else:
			last_three.append(m)
			last_three = last_three[1:]
		print(f"{str(m)} ", end="")
		if tuple(last_three) in [(4, "L", 6), (4, "R", 12), (6, "R", 4)]:
			print("\n\t",end="")
	print("\n")

	# FULL: "A", "B", "A", "C", "A", "B", "C", "B", "C", "A"
	# {
	# 	"A": ['L', 12, 'R', 4, 'R', 4, 'L', 6],
	# 	"B": ['L', 12, 'R', 4, 'R', 4, 'R', 12],
	# 	"C": ['L', 10, 'L', 6, 'R', 4],
	# }

	# Enough "showing our work", time to actually do the thing. The Program:
	main_routine = "A,B,A,C,A,B,C,B,C,A\n"
	function_a = "L,12,R,4,R,4,L,6\n"
	function_b = "L,12,R,4,R,4,R,12\n"
	function_c = "L,10,L,6,R,4\n"
	feed_mode = "n\n"
	full_program = [main_routine, function_a, function_b, function_c, feed_mode]
	
	# Initialize and boot up the controller:
	controller = ic.intcode_computer(input_lines[0])
	controller.prog[0] = 2
	for line in full_program:
		controller.run()
		while controller.output_pending():
			print(chr(controller.output()), end="")
		for c in line:
			print(c, end="")
			controller.input(ord(c))
	
	# With the program loaded, now we run the controller and output its ending
	# value: The dust it found. 
	controller.run()
	while controller.output_pending():
		c = controller.output()
		print(chr(c) if c < 1000 else c, end="")

	print("\n")