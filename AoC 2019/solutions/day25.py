import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(25)
except:
	input_lines = ["Input Lines Not Found"]
	pass

def do_part_two_for(lines):
	pass

def render_ship_map(room_map, room_exits, room_legend, pxy):
	expanded_map = collections.defaultdict(lambda: " ")
	for xy in room_map.keys():
		x = xy[0] * 3
		y = xy[1] * 3
		exits = room_exits[(x//3, y//3)]
		expanded_map[(x - 1, y - 1)] = " " 
		expanded_map[(x + 0, y - 1)] = "|" if "n" in exits else " "
		expanded_map[(x + 1, y - 1)] =  " "
		expanded_map[(x - 1, y + 0)] = "-" if "w" in exits else " "
		expanded_map[(x + 0, y + 0)] = chr(64+room_map[xy]) if xy != pxy else "*"
		expanded_map[(x + 1, y + 0)] = "-" if "e" in exits else " "
		expanded_map[(x - 1, y + 1)] = " "
		expanded_map[(x + 0, y + 1)] = "|" if "s" in exits else " "
		expanded_map[(x + 1, y + 1)] = " "
	
	all_coords = [k for k in expanded_map.keys()]
	MINX = all_coords[0][0]
	MAXX = all_coords[0][0]
	MINY = all_coords[0][1]
	MAXY = all_coords[0][1]
	for xy in all_coords:
		MINX = min(MINX, xy[0])
		MAXX = max(MAXX, xy[0])
		MINY = min(MINY, xy[1])
		MAXY = max(MAXY, xy[1])

	print("== MAP ==")
	for y in range(MINY, MAXY+1):
		print("\t", end="")
		for x in range(MINX, MAXX+1):
			print(f"{expanded_map[(x, y)]}", end="")
		print()
	print()

	print("== LEGEND ==\n - (*)\t== YOU ARE HERE ==")
	for ln in room_legend.keys():
		print(f" - ({ln})\t{room_legend[ln]}")
	print()

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"...They gave us a console-command RPG in intcode, and we have to pl"
       	  f"ay it to find the password for the main airlock!!! :D\n")

	print("Alright, I suppose... this is the game! :D\n")


	# Attempts to map this thing failed because not every movement is equivalent
	# IE: SOUTH -> EAST != EAST -> SOUTH. 

	# Despite this, I played the game and found that you need a mug, hypercube, 
	# astrolabe, and coin to get the password, which is 1077936448

	game = ic.intcode_computer(input_lines[0])
	command = ""
	ship_map = collections.defaultdict(int)
	ship_map_exits = collections.defaultdict(list)
	ship_map_legend = {}
	player_xy = (100, 100)
	room_ind = 1
	last_full_prompt = ""
	while command != "exit":
		game.run()
		prompt = ""

		# Read the Prompt. 
		while game.output_pending():
			prompt += chr(game.output())

		if prompt.startswith("\n\n\n=="):
			last_full_prompt = prompt

		# Interpret the room name
		lh = prompt.find("==")
		rh = prompt.find("==", lh + 1)
		if (lh, rh) != (-1, -1):
			room_name = prompt[lh:rh+2]
		
		# Record it in our map if it's new
		if player_xy not in ship_map.keys():
			ship_map[player_xy] = room_ind
			ship_map_legend[room_ind] = room_name
			room_ind += 1
			for dir in ["- north", "- south", '- east', '- west']:
				if prompt.find(dir) != -1:
					ship_map_exits[player_xy].append(dir[2])



		# Get the player's input. If it's for our wrapper of the game (exit, 
		# map, etc...) then don't feed it to the game, but interpret it. 
		command = input(prompt)
		if command == "exit":
			break
		elif command == "map":
			render_ship_map(ship_map,ship_map_exits, ship_map_legend, player_xy)

		if command == "north" and last_full_prompt.find("- north") != -1:
			player_xy = algos.vadd(player_xy, ( 0, -1))
		elif command == "south" and last_full_prompt.find("- south") != -1:
			player_xy = algos.vadd(player_xy, ( 0,  1))
		elif command == "west" and last_full_prompt.find("- west") != -1:
			player_xy = algos.vadd(player_xy, (-1,  0))
		elif command == "east" and last_full_prompt.find("- east") != -1:
			player_xy = algos.vadd(player_xy, ( 1,  0))

		for c in command:
			game.input(ord(c))
		game.input(10)

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"This is the prompt for Part Two of the problem.\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe <THING THEY WANT> is {results}\n")
