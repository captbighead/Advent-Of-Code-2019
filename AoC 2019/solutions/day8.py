import utilities.io as io

try:
	input_lines = io.read_input_as_lines(8)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["Example"]

def do_part_one_for(lines):
	# We're given that the image is streamed in from top left to bottom right in
	# layers of 25 pixels wide and 6 pixels tall. 
	SIZE = 25 * 6
	orig = lines[0]
	layers = [orig[i*SIZE:(i+1)*SIZE] for i in range(len(orig)//SIZE)]
	layers = [lyr.replace("0", "") for lyr in layers]
	layers.sort(key=lambda s: len(s), reverse=True)
	ones = len(layers[0]) - len(layers[0].replace("1",""))
	twos = len(layers[0]) - len(layers[0].replace("2",""))
	return ones * twos

def do_part_two_for(lines):
	SIZE = 25 * 6
	orig = lines[0]
	layers = [orig[i*SIZE:(i+1)*SIZE] for i in range(len(orig)//SIZE)]

	final = ""
	for idx in range(SIZE):
		for lyr in layers:
			if lyr[idx] != "2":
				final += " " if lyr[idx] == "0" else "X"
				break
		
	for y in range(6):
		for x in range(25):
			print(final[y*25 + x], end="")
		print()
	print()
			

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"A made-up digital image format is presented. In order to make sure "
       	  f"it's being parsed correctly, we need to report the number of 0s in "
		  f"the layer that has the most.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of 0s with the layer that has the most is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"For part two, we need to just render the image.\n")
	do_part_two_for(input_lines)
