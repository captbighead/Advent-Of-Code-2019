import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(18)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = [
	"########################", 
	"#@..............ac.GI.b#", 
	"###d#e#f################", 
	"###A#B#C################", 
	"###g#h#i################", 
	"########################", 
]

class search_state:
	def __init__(self, xy, found, unfound, vault, elapsed) -> None:
		self.xy = xy
		self.found = found
		self.unfound = unfound
		self.vault = vault
		self.elapsed = elapsed
	
	def child_states(self):
		vault = self.vault
		fastest = collections.defaultdict(lambda:999999)
		fastest[self.xy] = 0
		search_space = collections.deque([(self.xy, self.elapsed)])
		accessible = {}
		while len(search_space):
			probe = search_space.popleft()
			last_xy = probe[0]
			last_t = probe[1]

			for v in algos.unit_vectors():
				next_xy = algos.vadd(last_xy, v)
				next_t = last_t + 1

				# This is not a branch we want to explore if we've been here
				# before, or if it's a wall. 
				if fastest[next_xy] < next_t or vault[next_xy] == "#":
					continue

				# This is also not a branch we want to explore if it's a 
				# lock that we don't have a key for.
				locked = vault[next_xy].isupper()
				if locked and vault[next_xy].lower() in self.unfound:
					continue

				# This is a branch worth following. 
				search_space.append((next_xy, next_t))
				fastest[next_xy] = next_t

				# If this is a new key, then log it as accessible:
				if vault[next_xy] in self.unfound:
					accessible[vault[next_xy]] = next_xy
		
		# Now we have a couple of helpful dicts: accessible (key > xy), and
		# fastest (xy > time_to_xy)
		returned_states = []
		for k in accessible.keys():
			nf = self.found.copy()
			nf.add(k)
			nu = self.unfound.copy()
			nu.remove(k)
			ne = fastest[accessible[k]]
			new_state = search_state(accessible[k], nf, nu, vault, ne)
			returned_states.append(new_state)
		return returned_states

def parse_map(lines):
	vault = collections.defaultdict(lambda:"#")
	keys = set([])
	orig = (-1, -1)
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			vault[(x, y)] = lines[y][x]
			if lines[y][x].islower():
				keys.add(lines[y][x])
			elif lines[y][x] == "@":
				orig = (x, y)
	return (vault, keys, orig)

def hash_set_as_str(set_to_hash):
	return "".join(sorted(set_to_hash))

def do_part_one_for(lines):
	inputs = parse_map(lines)
	vault = inputs[0]
	keys = inputs[1]
	origin = inputs[2]
	
	best = {}
	space = collections.deque([search_state(origin, set([]), keys, vault, 0)])
	while len(space):
		next = space.popleft()
		next_hash = hash_set_as_str(next.found)
		
		if best.get((next_hash, next.xy), 999999) < next.elapsed:
			continue

		best[(next_hash, next.xy)] = next.elapsed
		for child in next.child_states():
			space.append(child)

	best_time = 999999999999
	for b in best.keys():
		if len(b[0]) == len(keys) and best[b] < best_time:
			best_time = best[b]
	return best_time


def do_part_two_for(lines):
	pass

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We are in an underground vault and need to collect a series of keys"
       	  f" in the fewest steps possible. Each key opens its corresponding doo"
		  f"r, so some keys are gated behind the retrieval of other keys.\n")

	results = do_part_one_for(example_lines)
	print(f"When we do part one for the example input:")
	print(f"\tThe the least number of steps possible is {results}")
	print(f"\tWe expected: 81\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe the least number of steps possible is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(example_lines)
	print(f"When we do part two for the example input:")
	print(f"\tThe <THING THEY WANT> is {results}")
	print(f"\tWe expected: <SOLUTION THEY WANT>\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
