import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(22)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["Example"]

def shuffle_algo(position, deck_size, lines):
	# Deal with increment N: next_pos = current_pos * N mod len
	# Cut N: next_pos = (current_pos - N) mod len
	# Deal into new stack: next_pos = (len - 1) - current_pos
	for line in lines:
		if line.startswith("deal i"):
			position = (deck_size - 1) - position
		elif line.startswith("deal w"):
			n = int(line.replace("deal with increment ", ""))
			position = (position * n) % deck_size
		elif line.startswith("cut"):
			n = int(line.replace("cut ", ""))
			position = (position - n) % deck_size
	return position


def do_part_one_for(lines):
	return shuffle_algo(2019, 10007, lines)

def do_part_two_for(lines):
	print("\tI'll come back to this one. The math is going over my head.")


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Using three different shuffling techniques, shuffle a standard deck"
       	  f" of 10007 space cards using the instructions given. Where is card 2"
		  f"019?\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tCard 2019 is in position: {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
