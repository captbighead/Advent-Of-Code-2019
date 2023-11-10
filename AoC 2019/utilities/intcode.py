import collections

class intcode_computer:

    def __init__(self, program, mem_allowance=10000) -> None:
        # Input sanitization
        if isinstance(program, str):
            program = [int(token) for token in program.split(",")]
        elif not isinstance(program, list):
            raise ValueError("Intcode program must be list or csv string")

        self.inst = 0
        self.halted = False
        self.suspended = False
        self.orig = collections.defaultdict(int)
        for i in range(len(program)):
            self.orig[i] = program[i]
        #self.mem_allowance = mem_allowance
        #self.orig.extend([0 for i in range(self.mem_allowance)])
        self.prog = self.orig.copy()
        self.qinp = collections.deque()
        self.qout = collections.deque()
        self.rel_base = 0

    def run(self, full_reset=False): 

        # If we were called after being suspended previously, then we need to
        # clarify that we're no longer suspended (until we try to do something
        # that suspends us again, at least :))
        if self.suspended:
            self.suspended = False

        # If we remember ourselves as halted, then we don't try to run again 
        # unless we're manually reset.
        if self.halted:
            return

        while self.inst < len(self.prog):
            # For ease of reference, alias the current opcode and parse the 
            # modes for its parameters (0 - Position Mode, 1 - Immediate Mode)
            op = self.prog[self.inst]
            p3mode = op // 10000    # Parameter mode for p3 (if applicable)
            op %= 10000
            p2mode = op // 1000     # Parameter mode for p2 (if applicable)
            op %= 1000
            p1mode = op // 100      # Parameter mode for p1 (if applicable)
            op %= 100               # The actual op is the last two digits

            # Define the values of parameters based on the opcode being used:
            # OPCODES WITH AT LEAST 1 PARAMETER
            if op in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                p1val = self.prog[self.inst + 1]
            else:
                p1val = None
            # OPCODES WITH AT LEAST 2 PARAMETERS
            if op in (1, 2, 5, 6, 7, 8):
                p2val = self.prog[self.inst + 2]
            else:
                p2val = None
            # OPCODES WITH 3 PARAMETERS
            if op in (1, 2, 7, 8):
                p3val = self.prog[self.inst + 3]
            else:
                p3val = None

            # Use Parameter modes to find the actual value for each parameter:
            if p1val == None:
                p1actual = None
            elif p1mode == 1:
                p1actual = p1val
            elif p1mode == 2:
                p1actual = self.prog[self.rel_base + p1val]
            elif p1mode == 0:
                p1actual = self.prog[p1val]

            if p2val == None:
                p2actual = None
            elif p2mode == 1:
                p2actual = p2val
            elif p2mode == 2:
                p2actual = self.prog[self.rel_base + p2val]
            elif p2mode == 0:
                p2actual = self.prog[p2val]

            # With the instructions as set, P3 always appears to be mode 0.
            
            # Perform the actual operations:
            # OPCODE 1: ADD
            if op == 1:
                if p3mode == 2:
                    self.prog[self.rel_base + p3val] = p1actual + p2actual
                else:
                    self.prog[p3val] = p1actual + p2actual
                self.inst += 4  # Takes 3 params, so we step 4

            # OPCODE 2: MULT
            elif op == 2:
                if p3mode == 2:
                    self.prog[self.rel_base + p3val] = p1actual * p2actual
                else:
                    self.prog[p3val] = p1actual * p2actual
                self.inst += 4  # Takes 3 params, so we step 4

            # OPCODE 3: INPUT
            elif op == 3:
                if len(self.qinp):
                    if p1mode == 2:
                        self.prog[self.rel_base + p1val] = self.qinp.popleft()
                    else:
                        self.prog[p1val] = self.qinp.popleft() 
                    #self.prog[p1val] = self.qinp.popleft()  # Position mode
                    self.inst += 2  # Takes 1 param, so we step 2
                else:
                    self.suspended = True
                    return  # Returning now preserves our current state

            # OPCODE 4: OUTPUT
            elif op == 4:
                self.qout.append(p1actual)
                self.inst += 2  # Takes 1 param, so we step 2

            # OPCODE 5: JUMP-IF-TRUE
            elif op == 5:
                if p1actual: 
                    self.inst = p2actual
                else:
                    self.inst += 3  # Takes 2 parameters, so we step 3

            # OPCODE 6: JUMP-IF-FALSE
            elif op == 6:
                if not p1actual: 
                    self.inst = p2actual
                else:
                    self.inst += 3  # Takes 2 parameters, so we step 3

            # OPCODE 7: LESS-THAN
            elif op == 7:
                if p3mode == 2:
                    if p1actual < p2actual:
                        self.prog[self.rel_base + p3val] = 1 
                    else:
                        self.prog[self.rel_base + p3val] = 0
                else:
                    self.prog[p3val] = 1 if p1actual < p2actual else 0
                self.inst += 4  # Takes 3 parameters, so we step 4

            # OPCODE 8: EQUALS
            elif op == 8:
                if p3mode == 2:
                    if p3mode == 2:
                        if p1actual == p2actual:
                            self.prog[self.rel_base + p3val] = 1 
                        else:
                            self.prog[self.rel_base + p3val] = 0
                else:
                    self.prog[p3val] = 1 if p1actual == p2actual else 0
                self.inst += 4  # Takes 3 parameters, so we step 4

            # OPCODE 9: RELATIVE BASE OFFSET
            elif op == 9:
                self.rel_base += p1actual
                self.inst += 2

            # OPCODE 99: HALT
            elif op == 99:
                self.halted = True
                break

        # If we were not told to reset explicitly, then we are meant to brick up
        # on the halt instruction. Preserve our state entirely and refuse to 
        # work again until manually reset
        if not full_reset:
            return

        # Otherwise, if we want to do a full factory reset, we can do that. 
        # Input and output queues are not maintained by the computer's run 
        # operations.
        if full_reset:
            self.inst = 0
            self.prog = self.orig.copy()
            self.halted = False

    def input(self, n):
        self.qinp.append(n)

    def output(self):
        return self.qout.popleft()
    
    def output_pending(self):
        return len(self.qout)

    