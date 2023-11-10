import utilities.io as io
import utilities.intcode as ic

try:
	input_lines = io.read_input_as_lines(2)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["1,1,1,4,99,5,6,0,99"]

def do_part_one_for(lines, example=False):
	comp = ic.intcode_computer([int(ln) for ln in lines[0].split(",")])
	if not example:
		comp.prog[1] = 12
		comp.prog[2] = 2
	comp.run()
	return comp.prog[0]

def do_part_two_for(lines):
	initial_memory = [int(ln) for ln in lines[0].split(",")]
	goal_out = 19690720
	for noun in range(100):
		for verb in range(100):
			comp = ic.intcode_computer(initial_memory.copy())
			comp.prog[1] = noun
			comp.prog[2] = verb
			comp.run()
			if comp.prog[0] == goal_out:
				return 100 * noun + verb

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We need to create an intcode computer to run diagnostics on some pr"
       	  f"ograms, and report the resulting value in position 0 of the compute"
		  f"r's memory.\n")

	results = do_part_one_for(example_lines, True)
	print(f"When we do part one for the example input:")
	print(f"\tThe returned value is {results}")
	print(f"\tWe expected: 30\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe returned value is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we need to find the noun/verb pair that yields the output 19690"
       	  f"720 when we plug them into the intcode computer with the given prog"
		  f"ram.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe noun/verb phrase is {results}\n")
