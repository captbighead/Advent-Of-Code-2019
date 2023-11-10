import utilities.intcode as ic
import utilities.algos as algos
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(11)
except:
	input_lines = ["Input Lines Not Found"]
	pass

example_lines = ["Example"]

class ehpr:

	def __init__(self, lines) -> None:
		self.brain = ic.intcode_computer(lines[0])
		self.camera = collections.defaultdict(lambda: 0)
		self.compass = algos.unit_vectors()
		self.compass_ind = 0
		self.xy = (0,0)
		self.painted_panels = set([])


	def operate(self):
		if not self.brain.halted:
			self.read_camera()
			self.paint()
			self.move()
		return self.brain.halted


	def read_camera(self):
		self.brain.qinp.append(self.camera[self.xy])


	def paint(self):
		self.brain.run()
		colour = self.brain.qout.popleft()
		self.camera[self.xy] = colour
		self.painted_panels.add(self.xy)


	def move(self):
		# Perform the turn as instructed
		dir = -1 if not self.brain.qout.popleft() else 1
		self.compass_ind += dir
		self.compass_ind %= 4

		# Actually move along the new axis
		self.xy = algos.vadd(self.xy, self.compass[self.compass_ind])

def do_part_one_for(lines):
	robot = ehpr(lines)
	while not robot.operate():
		continue
	return len(robot.painted_panels)

def do_part_two_for(lines):
	robot = ehpr(lines)
	robot.camera[(0, 0)] = 1
	while not robot.operate():
		continue
	def translation(x):
		return " " if x == 0 else "#"
	inverted = collections.defaultdict(int)
	for xy in robot.camera.keys():
		inverted[(xy[0], xy[1]*-1)] = robot.camera[xy]
	algos.print_map(inverted, translation=translation, PRINT_BOUND=80)

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"We need to paint our license plate number on our spaceship with a r"
       	  f"obot that has an intcode brain.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe number of panels painted at least once is {results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Now that we know how to start the robot on the right panel, we see "
       	  f"the license plate number it prints for us: \n")

	do_part_two_for(input_lines)
