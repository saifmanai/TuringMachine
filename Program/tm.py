
#tm.py: The base Turing Machine

import threading
import time

STEP_READ = 0
STEP_WRITE = 1
STEP_MOVE = 2
STEP_STATE = 3

class TuringProgram:
    def __init__(self, name):
        self.name = name

        #default values
        self.alphabet = "01"
        self.symbol_blank = '_'
        self.dir_left = '<'
        self.dir_right = '>'
        self.dir_none = '-'
        self.state_initial = 'init'
        self.state_final = 'halt'

        self.tapes = []
        self.actions = list()

    
    def set_alphabet(self, alphabet, blank):
        self.alphabet = alphabet
        self.symbol_blank = blank

    def set_directions(self, left, right, none):
        self.dir_left = left
        self.dir_right = right
        self.dir_none = none

    def set_limit_states(self, initial, final):
        self.state_initial = initial
        self.state_final = final

    def set_tapes(self, *arg):
        self.tapes = list(arg)
    
    def add_action(self, state, read_values, write_values, directions, next_state):
        self.actions.append(dict(id=len(self.actions), state=state, read_values=read_values, write_values=write_values, directions=directions, next_state=next_state))
        
    def set_actions(self, table):
        self.actions = list()
        for line in table.split('\n'):
            columns = line.split()
            state = columns[0]
            read_values = columns[1].split(',')
            write_values = columns[2].split(',')
            directions = columns[3].split(',')
            next_state = columns[4]
            self.add_action(state, read_values, write_values, directions, next_state)

    def get_action(self, state, read_values):
        for action_id, action in enumerate(self.actions):
            if action['state'] == state and action['read_values'] == read_values:
                return action
        return None


class TuringMachine(threading.Thread):
    def __init__(self, program=None, speed=4, listener=None):
        threading.Thread.__init__(self)
        
        self.program = program
        self.speed = speed
        self.listener = listener
        
        self.should_continue = threading.Event()

        
    def set_program(self, program):
        self.program = program


    def read(self, tape_nr):
        tape = self.program.tapes[tape_nr]
        return tape[self.tapes_pos[tape_nr]]

  
    def write(self, tape_nr, value):
        tape = self.program.tapes[tape_nr]
        tape[self.tapes_pos[tape_nr]] = value


    def move(self, tape_nr, direction):
        tape = self.program.tapes[tape_nr]
        if direction == self.program.dir_left:
            if self.tapes_pos[tape_nr] <= 0:  
                tape.insert(0, self.program.symbol_blank) 
                self.tapes_pos[tape_nr] = 0
            else: 
                self.tapes_pos[tape_nr] -= 1
        elif direction == self.program.dir_right: 
            self.tapes_pos[tape_nr] += 1
            if self.tapes_pos[tape_nr] >= len(tape): 
                tape.append(self.program.symbol_blank)
    
    
    def run(self):
        if self.program == None: raise RuntimeError("No program specified")

        self.tapes_pos = list()
        for i in range(len(self.program.tapes)):
            self.tapes_pos.append(0)

        for tape in self.program.tapes:
            if len(tape) == 0:
                tape.append(self.program.symbol_blank)
        
        self.state = self.program.state_initial
        self.running = True
        self.should_continue.set()
        
        while self.running:
            self.should_continue.wait()
            
            self.read_step()
            self.post_step(STEP_READ)
            
            self.write_step()
            self.post_step(STEP_WRITE)
            
            self.move_step()
            self.post_step(STEP_MOVE)
            
            self.state_change_step()
            self.post_step(STEP_STATE)


    def post_step(self, step_type):
        if self.listener != None:
            self.listener(self, step_type)
            
        if hasattr(self, 'error'):
            raise RuntimeError(self.error)
    
        if self.speed != -1:
                time.sleep(1/float(self.speed))

    
    def read_step(self):
        read_values = []
        for tape_nr, tape in enumerate(self.program.tapes): 
            read_values.append(self.read(tape_nr)) 
            
        self.action = self.program.get_action(self.state, read_values)
        if self.action == None:
            self.error = "No action defined for state '%(state)s' and values (%(read)s)" % dict(state=self.state, read=','.join(read_values))
            self.running = False
            
                
    def write_step(self):
        for tape_nr, tape in enumerate(self.program.tapes):
              self.write(tape_nr, self.action['write_values'][tape_nr])

    def move_step(self):
        for tape_nr, tape in enumerate(self.program.tapes):
            self.move(tape_nr, self.action['directions'][tape_nr])

    def state_change_step(self):
        self.state = self.action['next_state']
        if self.state == self.program.state_final:
            self.running = False



if __name__ == "__main__":
    tape = "0100101"
    print("Initial value: "+tape)
    
    inversion = TuringProgram("Inversion")
    inversion.set_tapes(list(tape))
    inversion.set_actions("""init 0 1 > init
                             init 1 0 > init
                             init _ _ - halt""")

    def print_tapes(tm, step_type):
        if step_type == STEP_READ:
            tcopy = list(tm.program.tapes[0])
            pos = tm.tapes_pos[0]
            tcopy.insert(pos, '[')
            tcopy.insert(pos+2, ']')
            print(''.join(tcopy))
        elif step_type == STEP_STATE and not tm.running:
            print("Final value (trimmed): " + (''.join(tm.program.tapes[0])).strip('_'))
            
    machine = TuringMachine(inversion, listener=print_tapes)
    machine.start()
    machine.join()
