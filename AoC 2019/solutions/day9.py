import utilities.io as io
import utilities.intcode as ic

try:
	input_lines = io.read_input_as_lines(9)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["Example"]

def do_part_one_for(lines):
	comp = ic.intcode_computer(lines[0])
	comp.qinp.append(1)
	comp.run()
	for result in comp.qout:
		print(f"{result}, ", end="")
	print()
	return comp.qout[-1]

def do_part_two_for(lines):
	comp = ic.intcode_computer(lines[0])
	comp.qinp.append(2)
	comp.run()
	return comp.qout[-1]

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We're making one last change to our intcode computer. We will run a"
       	  f" program, and the output printed is a list of all the operations th"
		  f"at are working incorrectly, along with their parameter modes, follo"
		  f"wed by a keycode to put into the AoC site.\n")
	results = do_part_one_for(input_lines)

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now that the computer is verified to be complete, we can run the pr"
       	  f"ogram to find out the coordinates of the distress signal.\n")

	results = do_part_two_for(input_lines)
	print(f"The signal is {results}\n")
