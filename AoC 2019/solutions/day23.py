import utilities.algos as algos
import utilities.intcode as ic
import utilities.io as io
import collections

try:
	input_lines = io.read_input_as_lines(23)
except:
	input_lines = ["Input Lines Not Found"]
	pass

class network_node:
		def __init__(self, code, address, registry) -> None:
			self.brain = ic.intcode_computer(code)
			self.address = address
			self.registry = registry
			self.registry[self.address] = self
			self.packet_queue = collections.deque([])
			self.brain.input(address)
			self.brain.run()

		def operate(self):
			pq = self.packet_queue
			br = self.brain

			packet = [-1]
			if len(pq):
				packet = [pq.popleft(), pq.popleft()]
			
			for p_bit in packet:
				br.input(p_bit)
			br.run()

			if not br.output_pending():
				return 0

			address = br.output()

			# This is the end condition!
			if address == 255:
				x = br.output()
				y = br.output()

				self.registry[address] = (x, y)
				
				return y

			x = br.output()
			y = br.output()

			self.registry[address].packet_queue.append(x)
			self.registry[address].packet_queue.append(y)

			return 0

def do_part_one_for(lines):
	reg = {}
	for i in range(50):
		network_node(lines[0], i, reg)

	i = 0
	finished = 0
	while not finished:
		finished = reg[i].operate()
		i = (i + 1) % 50
	
	return finished
		

def do_part_two_for(lines):
	reg = {}
	for i in range(50):
		network_node(lines[0], i, reg)
	reg[255] = ()

	sent_by_nat = set([])

	while True:
		for i in range(50):
			reg[i].operate()

		# Run the NAT
		queued_packets = sum([len(reg[i].packet_queue) for i in range(50)])
		if not queued_packets:
			reg[0].packet_queue.append(reg[255][0])
			reg[0].packet_queue.append(reg[255][1])
			nat_y = reg[255][1]
			if nat_y not in sent_by_nat:
				sent_by_nat.add(nat_y)
			else:
				return nat_y

def solve_p1():
	print(f"PART ONE\n--------\n")
	print(f"Make a network of 50 intcode computers that send packets to each ot"
       	  f"her. Report the y value of the first packet sent to address 255.\n")

	results = do_part_one_for(input_lines)
	print(f"When we do part one for the actual input:")
	print(f"\tThe y value for the first packet sent to address 255 was: "
       	  f"{results}\n")

def solve_p2():
	print(f"PART TWO\n--------\n")
	print(f"Implement a monitor at address 255. It stores only the last packet "
       	  f"sent to it, and when the entire network has no packets in its queue"
		  f", the monitor sends its packet to the first network node to kick up"
		  f" the system again. Which is the first y value that the monitor send"
		  f"s twice?\n")

	results = do_part_two_for(input_lines)
	print(f"When we do part two for the actual input:")
	print(f"\tThe y value repeated by the monitor is {results}\n")
