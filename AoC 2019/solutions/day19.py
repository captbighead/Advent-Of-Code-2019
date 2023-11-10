import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(19)
except:
	input_lines = ["Input Lines Not Found"]
	pass

def do_part_one_for(lines):
	grid = collections.defaultdict(lambda:" ")
	beam_checker = ic.intcode_computer(lines[0], mem_allowance=1999999)
	count = 0
	for y in range(50):
		for x in range(50):
			beam_checker.input(x)
			beam_checker.input(y)
			beam_checker.run(True)
			result = beam_checker.output()
			count += result
			grid[(x,y)] = " " if not result else "#"
	return count



def do_part_two_for(lines):
	beam_checker = ic.intcode_computer(lines[0])

	def scan(x, y):
		beam_checker.input(x)
		beam_checker.input(y)
		beam_checker.run(True)
		return beam_checker.output()

	# Trail the left-most edge of the beam. The first time that the space at 
	# (99, -99) + our point is also in the beam is the returned coords.
	y = 3
	x = 1
	while True:
		while True:
			on_edge = scan(x, y)
			if on_edge:
				opp_corner_check = scan(x + 99, y - 99)
				if opp_corner_check:
					return x * 10000 + y - 99
				break
			x += 1
		y += 1

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Use an intcode program to scan for whether or not a given x,y coord"
       	  f"inate is affected by a tractor beam, and find out how many x,y coor"
		  f"dinates in the range of x in [0,50], y in [0,50] are affected.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of affected coordinates is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Using the scanner module we created, find the coordinates of the to"
       	  f"p left corner of the first 100x100 square (aligned with the grid) t"
		  f"hat fits entirely in the area of the beam.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe coordinates (as one int) are {results}\n")
