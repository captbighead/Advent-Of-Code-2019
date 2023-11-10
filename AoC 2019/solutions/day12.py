import utilities.algos as algos
import utilities.io as io

try:
	input_lines = io.read_input_as_lines(12)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"<x=-1, y=0, z=2>", 
	"<x=2, y=-10, z=-7>", 
	"<x=4, y=-8, z=8>", 
	"<x=3, y=5, z=-1>"
]

#example_lines = [
#	"<x=-8, y=-10, z=0>", 
#	"<x=5, y=5, z=10>", 
#	"<x=2, y=-7, z=3>", 
#	"<x=9, y=-8, z=-3>"
#]

class moon_system:

	def __init__(self, blueprints, names) -> None:
		self.moons = []
		for i in range(len(blueprints)):
			moon = {"name":names[i]}
			bp = blueprints[i][1:-1].replace(",", "")
			moon["pos"] = [int(s[2:]) for s in bp.split(" ")]
			moon["vel"] = [0, 0, 0]
			self.moons.append(moon)
	
	def step(self):
		# Apply gravity to every pair of moons. 
		for i in range(4):
			for j in range(i+1, 4):
				mi = self.moons[i]
				mj = self.moons[j]
				for n in range(3):
					delta_n = mj["pos"][n] - mi["pos"][n]
					mi["vel"][n] += delta_n // abs(delta_n) if delta_n else 0
					mj["vel"][n] -= delta_n // abs(delta_n) if delta_n else 0
		
		# Apply velocity
		for i in range(4):
			for n in range(3):
				self.moons[i]["pos"][n] += self.moons[i]["vel"][n]

	
	def total_energy(self):
		e = 0
		for m in self.moons:
			pot = sum([abs(n) for n in m["pos"]])
			kin = sum([abs(n) for n in m["vel"]])
			e += pot * kin
		return e
	

	def tuple_for(self, index):
		out = []
		for m in self.moons:
			out.append(m["pos"][index])
			out.append(m["vel"][index])
		return tuple(out)


def parse_moons(lines):
	return moon_system(lines, ["Io", "Europa", "Ganymede", "Callisto"])


def do_part_one_for(lines, steps):
	moon_sys = parse_moons(lines)
	for i in range(steps):
		moon_sys.step()
	return moon_sys.total_energy()


def do_part_two_for(lines):
	moon_sys = parse_moons(lines)
	prime_sieve = algos.sieve_of_eratosthenes(300000)
	
	# Check for our return to our initial state
	initials = [moon_sys.tuple_for(i) for i in range(3)]
	periods = [-1 for i in range(3)]
	detected = [False for i in range(3)]
	t = 0
	while not (detected[0] and detected[1] and detected[2]):
		# Advance time.
		moon_sys.step()
		t += 1

		# Check for new cycle detections:
		for i in range(3):
			if not detected[i] and moon_sys.tuple_for(i) == initials[i]:
				detected[i] = True
				periods[i] = t
	
	return prime_sieve.least_common_multiple(periods)


	




def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Simulate the movement of 4 moons in 3D space, for a number of steps"
       	  f", and then output the total energy in the system after those steps."
		  f"\n")

	results = do_part_one_for(example_lines, 10)
	print(f"When run the example coordinates for 10 steps:")
	print(f"\tThe total energy is {results}")
	print(f"\tWe expected: 179\n")

	results = do_part_one_for(input_lines, 1000)
	print(f"When we run the actual coordinates for 1000 steps:")
	print(f"\tThe total energy is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Simulate the system until it repeats itself, where all moons are in"
       	  f" the same positions, with the same velocities as a previous point i"
		  f"n time.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe elapsed ticks before the first repeat is {results}")
	print(f"\tWe expected: 2772\n")
#	print(f"\tWe expected: 4686774924\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe elapsed ticks before the first repeat is {results}")
