import utilities.io as io

try:
	input_lines = io.read_input_as_lines(1)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["12", "14", "1969", "100756"]

def do_part_one_for(lines):
	sum_fuel = 0
	for mass in [int(ln) for ln in lines]:
		sum_fuel += mass // 3 - 2
	return sum_fuel

def do_part_two_for(lines):
	sum_fuel = 0
	for mass in [int(ln) for ln in lines]:
		fuel_current = max(mass // 3 - 2, 0)
		fuel_running = fuel_current

		# Keep iteratively reducing the fuel needed for the mass of the fuel we
		# just added. 
		while fuel_current > 0:
			fuel_current = max(fuel_current // 3 - 2, 0)
			fuel_running += fuel_current

		sum_fuel += fuel_running
	return sum_fuel

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We need to determine the amount of fuel needed to launch all of the"
       	   " modules on our spacecraft.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe sum of all of the fuel is {results}")
	print(f"\tWe expected: 34241\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe sum of all of the fuel is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"We didn't account for the fuel needed to launch the mass added by t"
       	  f"he fuel!\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe sum of all the fuel is actually {results}")
	print(f"\tWe expected: 51316\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe sum of all the fuel is actually {results}\n")
