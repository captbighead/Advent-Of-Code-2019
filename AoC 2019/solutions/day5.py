import utilities.io as io
import utilities.intcode as ic

try:
	input_lines = io.read_input_as_lines(5)
	example_lines = io.read_examples_as_lines(5)
except:
	input_lines = ["Input Lines Not Found"]
	example_lines = ["Input Lines Not Found"]

def do_part_one_for(lines):
	pass

def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We are expanding our Intcode Computer to take inputs and give outpu"
       	  f"ts, as well as process parameters in different modes (Position, whi"
		  f"ch was the default used in problem 2, or Immediate).\n")

	diagnostic_program = [int(token) for token in input_lines[0].split(",")]
	comp = ic.intcode_computer(diagnostic_program)
	comp.qinp.append(1)
	comp.run(True)
	
	print("To verify it's working, we give it a diagnostic code of 1 and assess"
       	 f" its output stream. The stream should be a list of 0s, followed by a"
		 f" diagnostic code to submit to the AoC website:\n")
	
	for val in comp.qout:
		tok = str(val) + (", " if not val else " ")
		print(f"{tok}", end="")
	print("\n")


def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"We are expanding our Intcode Computer to handle some control flow o"
       	  f"perations as well as comparisons of values. This should output only"
		  " a single value.\n")

	diagnostic_program = [int(token) for token in input_lines[0].split(",")]
	diagnostic_program_posmod = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
	diagnostic_program_immmod = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

	print("We're going to add some unit testing stuff in here. This is a progra"
       	 f"m that takes a number and outputs 0 if the input was 0, otherwise it"
		 f" outputs 1 (using positon mode):\n")
	
	comp_pos = ic.intcode_computer(diagnostic_program_posmod)
	comp_pos.qinp.append(0)
	comp_pos.run(True)
	print(f"When given the value 0, it gives us back: {comp_pos.qout.pop()}")
	comp_pos.qinp.append(1)
	comp_pos.run(True)
	print(f"When given the value 1, it gives us back: {comp_pos.qout.pop()}\n")

	print(f"This is a program that takes a number and outputs 0 if the input wa"
       	  f"s 0, otherwise it outputs 1 (using immediate mode):\n")
	
	comp_imm = ic.intcode_computer(diagnostic_program_immmod)
	comp_imm.qinp.append(0)
	comp_imm.run(True)
	print(f"When given the value 0, it gives us back: {comp_imm.qout.pop()}")
	comp_imm.qinp.append(1)
	comp_imm.run(True)
	print(f"When given the value 1, it gives us back: {comp_imm.qout.pop()}\n")

	large_ex = [
		3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,
	    98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,
		4,20,1105,1,46,98,99
	]
	comp_large = ic.intcode_computer(large_ex)
	print(f"Now we'll run it on a larger example. This one takes a number and o"
       	  f"utputs 999 if the number is below 8, 1000 if the number is 8, and 1"
		  f"001 if it's greater than 8.\n")
	comp_large.qinp.append(7)
	comp_large.run(True)
	print(f"  - When the input was 7:\t{comp_large.qout.pop()}")
	comp_large.qinp.append(8)
	comp_large.run(True)
	print(f"  - When the input was 8:\t{comp_large.qout.pop()}")
	comp_large.qinp.append(9)
	comp_large.run(True)
	print(f"  - When the input was 9:\t{comp_large.qout.pop()}\n")

	comp = ic.intcode_computer(diagnostic_program)
	comp.qinp.append(5)
	comp.run(True)
	
	print("To verify it's working, we give it a diagnostic code of 5 and assess"
       	 f" its output stream. The stream should be just a single diagnostic co"
		 f"de to submit to the AoC website:\n\n{comp.qout.popleft()}\n")
