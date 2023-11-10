import utilities.io as io
import utilities.intcode as ic
import utilities.algos as algos

try:
	input_lines = io.read_input_as_lines(7)
except:
	input_lines = ["Input Lines Not Found"]
	pass 

example_lines = io.read_examples_as_lines(7)
p2_prog = ["3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,2" +
	   	   "8,1005,28,6,99,0,0,5"]

def do_part_one_for(lines):
	configs = algos.permutations([v for v in range(5)])
	acs = ic.intcode_computer(lines[0])
	best_config = ([0,0,0,0,0], -9999)
	for config in configs:
		signal_str = 0
		for phase in config:
			acs.qinp.append(phase)
			acs.qinp.append(signal_str)
			acs.run(True)
			signal_str = acs.qout.pop()
		if signal_str > best_config[1]:
			best_config = (config, signal_str)
	return best_config

def do_part_two_for(lines):
	configs = algos.permutations([v for v in range(5, 10)])
	best_config = ([0,0,0,0,0], -9999)
	for config in configs:
		acs_array = [ic.intcode_computer(lines[0]) for i in range(5)]
		for i in range(5):
			acs_array[i].qinp.append(config[i])
		acs_array[-1].qout.append(0)
		acs_ind = 0

		while not acs_array[acs_ind].halted:
			acs_prior = (acs_ind - 1) % 5
			acs_array[acs_ind].qinp.append(acs_array[acs_prior].qout.popleft())
			acs_array[acs_ind].run()
			acs_ind = (acs_ind + 1) % 5
		
		signal_str = acs_array[-1].qout.pop()
		if signal_str > best_config[1]:
			best_config = (config, signal_str)
	return best_config


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We need to configure a series of amplifiers to get the best signal "
       	  f"output we can.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe best possible signal is {results[1]}, which came from the pha"
		  f"se setting configuration: {results[0]}")
	print(f"\tWe expected: 65210, from phase setting configuration: [1, 0, 4, 3"
       	  f", 2]\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe best possible signal is {results[1]}, which came from the pha"
		  f"se setting configuration: {results[0]}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"In part 2, we keep all computers for each amplifier distinct and do"
       	  f" not reset them between runs, running them in a feedback loop until"
		  f" they halt.\n")

	results = do_part_two_for(p2_prog)
	print(f"When we do part two for the example input:")
	print(f"\tThe best possible signal is {results[1]}, which came from the pha"
		  f"se setting configuration: {results[0]}")
	print(f"\tWe expected: 139629729, from phase setting configuration: [9, 8, "
       	  f"7, 6, 5]\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe best possible signal is {results[1]}, which came from the pha"
		  f"se setting configuration: {results[0]}\n")
