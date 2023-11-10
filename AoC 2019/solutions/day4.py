import utilities.io as io
import collections

input_range = range(347312, 805915)
#input_range = [111111, 223450, 123789]

def do_part_one_for(irange):
	valids = 0
	for pot_pwd in irange:
		pwd = str(pot_pwd)
		asc = True
		dub = False
		for i in range(len(pwd)-1):
			asc = asc and int(pwd[i]) <= int(pwd[i+1])
			pwdi = pwd[i]
			pwdi1 = pwd[i+1]
			dub = dub or pwdi == pwdi1
		valids += 1 if asc and dub else 0
	return valids
		

def do_part_two_for(irange):
	valids = 0
	for pot_pwd in irange:
		pwd = str(pot_pwd)

		asc = True
		for i in range(len(pwd)-1):
			asc = asc and int(pwd[i]) <= int(pwd[i+1])
			
		freq = collections.defaultdict(lambda:0)
		for char in pwd:
			freq[char] += 1
		dub = False
		for char in freq.keys():
			dub = dub or freq[char] == 2

		valids += 1 if asc and dub else 0
	return valids

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"How many of the numbers in the input range are valid passwords?\n")

	results = do_part_one_for(input_range)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of valid passwords is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(input_range)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
