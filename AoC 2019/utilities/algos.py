import collections
import heapq
import math

class sieve_of_eratosthenes:

	def __init__(self, limit=10000) -> None:
		self.limit = limit
		lookup = {p: True for p in range(2, limit+1)}
		check_deque = collections.deque(sorted(lookup.keys()))

		while len(check_deque):
			p = check_deque.popleft()
			if not lookup[p]:
				continue

			n = p
			while n + p <= limit:
				n = n + p
				lookup[n] = False
		self.primes = set([p for p in lookup.keys() if lookup[p]])
	
	def is_prime(self, n):
		if n > self.limit:
			raise ValueError(f"{n} is out of bounds for the prime generator")
		return n in self.primes
	
	def primes_under(self, n):
		if n > self.limit:
			raise ValueError(f"{n} is out of bounds for the prime generator")
		return sorted([p for p in self.primes if p < n])


	def least_common_multiple(self, numbers):
		if max(numbers) > self.limit:
			raise ValueError(f"{max(numbers)} is out of bounds for the prime ge"
		    				 f"nerator")
		primes = self.primes_under(max(numbers)+1)
		prime_factors = {}
		for n in numbers:
			# Prime Factorization, starting with the lowest prime (2), divide 
			# the number n by every prime that divides it, and keep doing so 
			# until that prime (p) no longer divides it. Store every p and the 
			# power it is multiplied by.
			#
			# Since we're building the LCM, we only store every prime factor to
			# the highest power it has in its compositions of the numbers. 
			working_n = n
			for p in primes:
				p_pow = 0
				while working_n % p == 0 and working_n >= p:
					p_pow += 1
					working_n //= p
				
				# Store p at the highest power it was seen at amongst numbers n
				if p_pow > 0:
					current_max_power = prime_factors.get(p, 0)
					prime_factors[p] = max(p_pow, current_max_power)
		
		return math.prod([p ** prime_factors[p] for p in prime_factors])


def vadd(v, w):
	return tuple([v[i] + w[i] for i in range(len(v))])


def unit_vectors():
	return [(0, 1), (1, 0), (0, -1), (-1, 0)]


def unit_vectors_labelled(invert_y=False):
	if not invert_y:
		return {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}
	else:
		return {"D": (0, 1), "R": (1, 0), "U": (0, -1), "L": (-1, 0)}


def distance_manhattan(v, w):
	return sum([abs(v[i] - w[i]) for i in range(len(v))])


def permutations(values, completed=[], used=[], remaining=[]):
	# In the first call, set up the list of remaining values to be the full list
	if len(used) == 0:
		remaining = values.copy()
		completed = []

	# Iterate over the values we still need to create permutations with for this
	# wip permutation 'used'.
	for r in remaining:
		new_used = used.copy()
		new_used.append(r)
		new_rem = remaining.copy()
		new_rem.remove(r)

		# Either new_used is a completed permutation, or we need to keep going.
		if len(new_used) == len(values):
			completed.append(new_used)
		else:
			permutations(values, completed, new_used, new_rem)
	
	return completed


def print_map(map, translation=lambda x: x, prefix="\t", PRINT_BOUND=40):
	all_coords = [k for k in map.keys()]
	MINX = all_coords[0][0]
	MAXX = all_coords[0][0]
	MINY = all_coords[0][1]
	MAXY = all_coords[0][1]
	for xy in all_coords:
		MINX = min(MINX, xy[0])
		MAXX = max(MAXX, xy[0])
		MINY = min(MINY, xy[1])
		MAXY = max(MAXY, xy[1])

	if MAXX - MINX > PRINT_BOUND or MAXY - MINY > PRINT_BOUND:
		print(f"[Couldn't render map in a {PRINT_BOUND}x{PRINT_BOUND} square or"
			  f" less]\n")
		return

	for y in range(MINY, MAXY+1):
		print(prefix, end="")
		for x in range(MINX, MAXX+1):
			print(f"{translation(map[(x,y)])}", end="")
		print()
	print()
	return


def dijkstra(space, is_goal, is_impassible, origin=(0,0)):
	unvisited = [xy for xy in space.keys() if not is_impassible(xy)]
	visited = set([])
	paths = collections.defaultdict(lambda:None)
	paths[origin] = collections.deque([])

	def path_cost(dest):
		return len(paths[dest]) if paths[dest] != None else 999999999

	while len(unvisited):
		unvisited.sort(key=path_cost)
		next = unvisited.pop(0)
		path_here = paths[next]
		visited.add(next)

		# If we're visiting our goal, then we're done.
		if is_goal(next):
			return path_here
		
		# If the path here doesn't exist, then it's unreachable, and we're also
		# done.
		if path_here == None:
			return None

		# Otherwise, update the paths of the spaces adjacent to this node where
		# applicable. 
		for v in unit_vectors():
			adj = vadd(next, v)
			if adj in visited or is_impassible(adj):
				continue

			# Replace the path to the space if our path is more direct, or if
			# the path doesn't exist
			if paths[adj] == None or len(paths[adj]) > (len(path_here) + 1):
				path_adj = path_here.copy()
				path_adj.append(v)
				paths[adj] = path_adj

	raise ValueError("Could not find the goal.")

