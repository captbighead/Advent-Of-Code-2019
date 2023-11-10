import utilities.algos as algos
import utilities.io as io
import collections
import math

try:
	input_lines = io.read_input_as_lines(10)
except:
	input_lines = ["Input Lines Not Found"]
	pass
 
example_lines = [
	"......#.#.", "#..#.#....", "..#######.", ".#.#.###..", ".#..#.....", 
	"..#....#.#", "#..#....#.", ".##.#..###", "##...#..#.", ".#....####"
]

def generate_slopes(MAX_DIM):
	# Quick Prime generation
	primes = set([])
	sieve = set([n for n in range(2, MAX_DIM+1)])
	while len(sieve):
		p = min(sieve)
		max_sieve = max(sieve)
		sieve.remove(p)
		primes.add(p)
		c = p
		while c + p <= max_sieve:
			c += p
			if c in sieve:
				sieve.remove(c)

	# Generate all the slopes
	all = list(range(MAX_DIM+1))
	primes = sorted(list(primes))
	slopes = set([(0,1)])
	for d in all:
		for n in all:
			if n == 0:
				continue
			if n > d:
				break
			slope = (n, d)
			for p in primes:
				if p > min(n, d):
					break
				while (slope[0]%p, slope[1]%p) == (0, 0):
					slope = (slope[0]//p, slope[1]//p)
			slopes.add(slope)
	slopes = list(slopes)
	slopes_recip = [(xy[1], xy[0]) for xy in slopes if xy != (1,1)]
	slopes.extend(slopes_recip)
	slopes = sorted(slopes, key=lambda xy: xy[0]/xy[1] if xy[1] else 0)
	slopes_orig = slopes.copy()
	for quad in [(-1, 1), (1, -1), (-1, -1)]:
		slopes_quad = [(s[0]*quad[0], s[1]*quad[1]) for s in slopes_orig]
		slopes.extend(slopes_quad)
	return slopes

def do_part_one_for(lines):
	# Build our data structure: a coordinate pair mapped to the asteroids we can
	# see from it, and a deque of unknown coordinate pairs
	queue = collections.deque([])
	space = collections.defaultdict(lambda:None)
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			if lines[y][x] == "#":
				space[(x, y)] = 0
				queue.append((x, y))

	# Store the longest dimension of our asteroid field. When we generate a 
	# check where both x and y are greater than MAX_DIM, we know we're out of 
	# bounds for sure. 
	MAX_DIM = max(len(lines), len(lines[0]))
	
	# Strategy: iterate over every unchecked asteroid, and from it, try 
	# following every slope until we find our first asteroid or go out of bounds
	slopes = generate_slopes(MAX_DIM)
	while(len(queue)):
		ast = queue.popleft()
		seen = set([])
		for s in slopes:
			chk = algos.vadd(ast, s)
			while max([abs(n) for n in chk]) <= MAX_DIM and space[chk] == None:
				chk = algos.vadd(chk, s)
			if space[chk] != None:
				seen.add(chk)
		space[ast] = len(seen)
	
	# space now stores every asteroid and the count of slopes it checked that 
	# found an asteroid; ie: the asteroids it could see. Return the space and
	# number of visible slopes:
	most_visibles = max(space.keys(), key=lambda xy: space[xy] if space[xy] != None else 0)
	return (most_visibles, space[most_visibles])


def do_part_two_for(lines, station):
	MAX_DIM = max(len(lines), len(lines[0]))
	slopes = generate_slopes(MAX_DIM)
	slopes = set(slopes)
	def deg_from_neg_y(coord):
		return (450 + math.atan2(coord[1], coord[0]) * 180 / math.pi) % 360
	slopes = sorted(list(slopes), key=deg_from_neg_y)

	# Build our space
	space = {}
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			space[(x,y)] = lines[y][x]
	def inbounds(xy):
		return space.get(xy, "!") != "!"
	
	# Perform 200 obliterations
	last_destroyed = (-1,-1)
	angle_ind = 0
	for i in range(200):
		# Try every slope in order
		hit = False
		while not hit:
			slope = slopes[angle_ind%len(slopes)]
			chk = algos.vadd(station, slope)
			while inbounds(chk) and space[chk] != "#":
				chk = algos.vadd(chk, slope)
			if inbounds(chk):
				last_destroyed = chk
				space[chk] = "."
				hit = True
			angle_ind += 1
	
	return last_destroyed



	


	


def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Given a clustered grid of asteroids, find out how many are visible "
       	  f"from each point and report the point with the most visible asteroid"
		  "s.\n")

	results_ex = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe asterod that sees the most asteroids is {results_ex[0]}, seei"
       	  f"ng a total of {results_ex[1]} asteroids.")
	print(f"\tWe expected: (5, 8), seeing a total of 33 asteroids. \n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe asterod that sees the most asteroids is {results[0]}, seeing "
       	  f"a total of {results[1]} asteroids.")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"From the station found before, we are going to systematically blow "
       	  f"up asteroids in a clockwise arc. What is the coordinate of the 200t"
		  f"h asteroid vapourized this way?\n")

	results = do_part_two_for(input_lines, do_part_one_for(input_lines)[0])
	print(f"When we do part two for the actual input:")
	print(f"\tThe 200th asteroid destroyed is {results}\n")
