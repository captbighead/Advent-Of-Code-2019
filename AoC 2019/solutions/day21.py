import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(21)
except:
	input_lines = ["Input Lines Not Found"]
	pass

def do_part_one_for(lines):
	droid = ic.intcode_computer(lines[0])
	droid.run()
	final = False
	
	walk_program = [
		"NOT A T\n"
		"OR T J\n"
		"NOT B T\n"
		"OR T J\n"
		"NOT C T\n"
		"OR T J\n"
		"NOT D T\n"
		"NOT T T\n"
		"AND T J\n"
		"WALK\n"
	]

	#for i in range(16):	# Will up to take 15 instructions, then a WALK
	#	droid.run()
	#	
	#	# Get the droid's prompt and print it
	#	while(droid.output_pending()):
	#		print(f"{chr(droid.output())}", end="")
	#	
	#	# Take the input from the user and stream it to the droid
	#	input_stream = input()
	#	for c in input_stream:
	#		droid.input(ord(c))
	#	droid.input(10)
	#
	#	if input_stream == "WALK":
	#		droid.run()
	#		break

	for inst in walk_program:
		# Consume the prompt
		print(inst, end="")
		while droid.output_pending():
			droid.output()
		for c in inst:
			droid.input(ord(c))
		droid.run()
	
	# Display the results of the experiment
	print()
	while droid.output_pending():
		c = droid.output()
		if c > 255:
			print()
			return c
		print(f"{chr(c)}", end="")
	return -1
	

def do_part_two_for(lines):
	droid = ic.intcode_computer(lines[0])

	# Can you land D and (can you land H or E is ground)? 

	run_program = [
		"NOT A T\n",	# T -> A IS HOLE
		"OR T J\n",		# J -> A IS HOLE
		"NOT B T\n",	# T -> B IS HOLE
		"OR T J\n",		# J -> B IS HOLE OR A IS HOLE
		"NOT C T\n",	# T -> C IS HOLE
		"OR T J\n",		# J -> C IS HOLE OR B IS HOLE OR A IS HOLE
		"NOT D T\n",	# T -> D IS HOLE
		"NOT T T\n",	# T -> D IS GROUND
		"AND T J\n",	# J -> A, B, OR C IS HOLE AND D IS GROUND

		"NOT E T\n" 	# T -> E IS HOLE
		"NOT T T\n",	# T -> E IS GROUND
		"OR H T\n",		# T -> H IS GROUND OR E IS GROUND 
		"AND T J\n"		# J -> A, B, OR C IS HOLE, D IS GROUND, H OR E IS GROUND
		
		"RUN\n"
	]

	for inst in run_program:
		# Consume the prompt
		print(inst, end="")
		while droid.output_pending():
			droid.output()
		for c in inst:
			droid.input(ord(c))
		droid.run()
	
	# Display the results of the experiment
	print()
	while droid.output_pending():
		c = droid.output()
		if c > 255:
			print()
			return c
		print(f"{chr(c)}", end="")
	return -1


	#for i in range(16):	# Will up to take 15 instructions, then a RUN
	#	droid.run()
	#	
	#	# Get the droid's prompt and print it
	#	while(droid.output_pending()):
	#		print(f"{chr(droid.output())}", end="")
	#	
	#	# Take the input from the user and stream it to the droid
	#	input_stream = input()
	#	for c in input_stream:
	#		droid.input(ord(c))
	#	droid.input(10)
	#
	#	if input_stream == "RUN":
	#		droid.run()
	#		break
	#
	## Display the results of the experiment
	#print()
	#while droid.output_pending():
	#	c = droid.output()
	#	if c > 255:
	#		print()
	#		return c
	#	print(f"{chr(c)}", end="")
	#return -1

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"This is the prompt for Part One of the problem.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe recorded damage to the hull is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
