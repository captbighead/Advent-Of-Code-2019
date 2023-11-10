import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io

try:
	input_lines = io.read_input_as_lines(13)
except:
	input_lines = ["Input Lines Not Found"]
	pass

def do_part_one_for(lines):
	game = ic.intcode_computer(lines[0])
	game.run()
	screen = {}
	q = game.qout
	while len(q):
		x = q.popleft()
		y = q.popleft()
		t = q.popleft()
		screen[(x, y)] = t
	return sum([1 for p in screen.keys() if screen[p] == 2])


def do_part_two_for(lines, play=True):
	# Translates the tile classes to characters. 
	def renderer(tile):
		if tile == 0:
			return " "
		elif tile == 1:
			return "#"
		elif tile == 2:
			return "X"
		elif tile == 3: 
			return "_"
		elif tile == 4:
			return "O"

	game = ic.intcode_computer(lines[0])
	game.prog[0] = 2
	q = game.qout
	i = game.qinp
	screen = {}
	score = 0
	ball = (-1, -1)
	paddle = (-1, -1)

	# Read the screen updates
	while not game.halted:
		game.run()
		while len(q):
			x = q.popleft()
			y = q.popleft()
			t = q.popleft()

			# Don't try to draw the score with the tiles
			if x == -1:
				score = t
				continue

			# Update the positions of the ball and the paddle for the 'AI'
			if t == 4:
				ball = (x, y)
			if t == 3:
				paddle = (x, y)

			screen[(x, y)] = t

		if play:
			# Print the screen and the score as seperate commands. 
			algos.print_map(screen, renderer, PRINT_BOUND=60)
			print(f"SCORE: {score}\n")
			
			# Get input from the player
			inp = -2
			while inp not in (-1, 0, 1):
				inp = int(input("Joystick Position: "))
			i.append(inp)
		
		else:
			tilt = ball[0] - paddle[0]
			tilt = tilt // abs(tilt) if tilt else 0
			i.append(tilt)
	
	return score
	

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We have been given an intcode program that renders an arcade game. "
       	  f"To test our understanding of it, how many block tiles are on the sc"
		  f"reen when the game exits?\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of block tiles is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now we need to play the game and win (or more accurately, program a"
       	  f" bot to do it).\n")

	results = do_part_two_for(input_lines, False)
	print(f"When we do part two for the actual input:")
	print(f"\tThe winning score is {results}\n")
