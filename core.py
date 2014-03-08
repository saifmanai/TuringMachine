class TuringException(Exception): 
    def __init__(self, value): 
        Exception.__init__(self) 
        self.value = value 
    def __str__(self): 
        return self.value 
  
class TuringSetupException(TuringException): 
    pass
  
class TuringRuntimeException(TuringException): 
    pass
  
  
class TuringMachine: 
    def __init__(self, state_initial=0, state_halt='h', alphabet=(' ',0,1), symbol_nowrite='-', dir_left='<', dir_right='>', dir_stay='-'): 
        self.alphabet = alphabet
        self.symbol_blank = self.alphabet[0]
        self.symbol_nowrite = symbol_nowrite
        self.state_initial = state_initial 
        self.state_halt = state_halt 
        self.dir_left = dir_left 
        self.dir_right = dir_right 
        self.dir_stay = dir_stay
          
        self.tapes = []
        self.stacks = []
        self.actions = {}
        self.nr_actions = 0
    
    def add_tape(self, tape):
        if not type(tape) is list:
            raise TuringSetupException("tape is not of type 'list'")
        for symbol in tape:
            if not symbol in self.alphabet:
                raise TuringSetupException("Invalid symbol %s" % symbol)
        
        if len(tape) == 0: tape.append(self.symbol_blank)
        self.tapes.append(dict(tape=tape, position=0)) 

    def add_stack(self, stack):
        if not type(stack) is list: raise TuringSetupException("stack is not of type 'list'")  
        self.stacks.append(stack)
    
    def add_action(self, state, read_values, pop_values, write_values, push_values, directions, next_state): 
        read_values = tuple(read_values)
        pop_values = tuple(pop_values)
        
        for direction in directions: 
            if direction != self.dir_left and direction != self.dir_right and direction != self.dir_stay:  raise TuringSetupException("Invalid direction '%s'" % direction) 
  
        self.actions[(state, read_values, pop_values)] = dict(id=self.nr_actions, write_values=write_values, push_values=push_values, directions=directions, next_state=next_state)
        self.nr_actions += 1
    
    def _read(self, tape_nr):
        tape_entry = self.tapes[tape_nr]
        return tape_entry['tape'][ tape_entry['position'] ] 
  
    def _write(self, tape_nr, value):
        if value != self.symbol_nowrite:
            tape_entry = self.tapes[tape_nr]
            tape_entry['tape'][ tape_entry['position'] ] = value

    def _pop(self, stack_nr):
        stack = self.stacks[stack_nr]
        if len(stack) == 0:
            return self.symbol_blank
        else:
            return stack.pop()

    def _push(self, stack_nr, value):
        if value != self.symbol_nowrite:
            stack = self.stacks[stack_nr]
            stack.append(value)
            
    def _move(self, tape_nr, direction):
        tape_entry = self.tapes[tape_nr]
        if direction == self.dir_left: 
            if tape_entry['position'] <= 0:  
                tape_entry['tape'].insert(0, self.symbol_blank) 
                tape_entry['position'] = 0
            else: 
                tape_entry['position'] -= 1
        elif direction == self.dir_right: 
            tape_entry['position'] += 1
            if tape_entry['position'] >= len(tape_entry['tape']): 
                tape_entry['tape'].append(self.symbol_blank)
        elif direction != self.dir_stay:
            raise TuringRuntimeException("Invalid direction '%(dir)s' for state '%(state)s' and values (%(read)s), (%(pop)s)" % dict(dir=direction, state=self.state, read=read_values, pop=pop_values))
  
    def run_step(self):
        if self.state == self.state_halt:
            return
        
        read_values = [] 
        for tape_nr, tape_entry in enumerate(self.tapes): 
            read_values.append(self._read(tape_nr)) 
        read_values = tuple(read_values)

        pop_values = [] 
        for stack_nr, stack in enumerate(self.stacks): 
            pop_values.append(self._pop(stack_nr)) 
        pop_values = tuple(pop_values) 
          
        index = (self.state, read_values, pop_values) 
        if not index in self.actions: raise TuringRuntimeException("No action defined for state '%(state)s' and values (%(read)s), (%(pop)s)" % dict(state=self.state, read=read_values, pop=pop_values)) 
          
        action = self.actions[index]

        self.current_action = action['id']
        
        for tape_nr, tape_entry in enumerate(self.tapes):
            self._write(tape_nr, action['write_values'][tape_nr])

        for stack_nr, stack in enumerate(self.stacks):
            self._push(stack_nr, action['push_values'][stack_nr])
        
        for tape_nr, tape_entry in enumerate(self.tapes):
            self._move(tape_nr, action['directions'][tape_nr]) 
          
        self.state = action['next_state'] 

        if self.state == self.state_halt:
            self.current_action = -1
        
    def init(self):
        if len(self.tapes) == 0: raise TuringRuntimeException("No tapes defined!") 
        if len(self.actions) == 0: raise TuringRuntimeException("No actions defined!") 
          
        self.state = self.state_initial
        self.current_action = -1
      
    def run(self): 
        while self.state != self.state_halt:
            self.run_step()
  
  
if __name__ == "__main__": 
    blank=' '
    nowrite = '-'
    tape1 = [1,0,1,1,1,0]
    tape2 = [1,0,1,1,0,0]
    tape3 = [' ']
    print(tape1)
    print(tape2)

    tm = TuringMachine(alphabet = (blank,0,1), symbol_nowrite = nowrite)
    
    tm.add_tape(tape1)
    tm.add_tape(tape2)
    tm.add_tape(tape3)
    tm.add_stack([0])
    
    tm.add_action(0, [0,0,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','>','>'], 0)
    tm.add_action(0, [0,1,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','>','>'], 0)
    tm.add_action(0, [1,0,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','>','>'], 0)
    tm.add_action(0, [1,1,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','>','>'], 0)
    tm.add_action(0, [blank,0,blank], [0], [nowrite, nowrite, nowrite], [0], ['-','>','>'], 0)
    tm.add_action(0, [blank,1,blank], [0], [nowrite, nowrite, nowrite], [0], ['-','>','>'], 0)
    tm.add_action(0, [0,blank,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','-','>'], 0)
    tm.add_action(0, [1,blank,blank], [0], [nowrite, nowrite, nowrite], [0], ['>','-','>'], 0)
    tm.add_action(0, [blank,blank,blank], [0], [nowrite, nowrite, nowrite], [0], ['-','-','-'], 1)

    tm.add_action(1, [blank,blank,blank], [0], [nowrite, nowrite, nowrite], [0], ['<','<','<'], 2)

    tm.add_action(2, [0,0,blank], [0], [nowrite, nowrite, 0], [0], ['<','<','<'], 2)
    tm.add_action(2, [0,1,blank], [0], [nowrite, nowrite, 1], [0], ['<','<','<'], 2)
    tm.add_action(2, [1,0,blank], [0], [nowrite, nowrite, 1], [0], ['<','<','<'], 2)
    tm.add_action(2, [1,1,blank], [0], [nowrite, nowrite, 0], [1], ['<','<','<'], 2)

    tm.add_action(2, [0,0,blank], [1], [nowrite, nowrite, 1], [0], ['<','<','<'], 2)
    tm.add_action(2, [0,1,blank], [1], [nowrite, nowrite, 0], [1], ['<','<','<'], 2)
    tm.add_action(2, [1,0,blank], [1], [nowrite, nowrite, 0], [1], ['<','<','<'], 2)
    tm.add_action(2, [1,1,blank], [1], [nowrite, nowrite, 1], [1], ['<','<','<'], 2)

    tm.add_action(2, [blank,0,blank], [0], [nowrite, nowrite, 0], [0], ['-','<','<'], 2)
    tm.add_action(2, [blank,1,blank], [0], [nowrite, nowrite, 1], [0], ['-','<','<'], 2)
    tm.add_action(2, [0,blank,blank], [0], [nowrite, nowrite, 0], [0], ['<','-','<'], 2)
    tm.add_action(2, [1,blank,blank], [0], [nowrite, nowrite, 1], [0], ['<','-','<'], 2)

    tm.add_action(2, [blank,0,blank], [1], [nowrite, nowrite, 1], [0], ['-','<','<'], 2)
    tm.add_action(2, [blank,1,blank], [1], [nowrite, nowrite, 0], [1], ['-','<','<'], 2)
    tm.add_action(2, [0,blank,blank], [1], [nowrite, nowrite, 1], [0], ['<','-','<'], 2)
    tm.add_action(2, [1,blank,blank], [1], [nowrite, nowrite, 0], [1], ['<','-','<'], 2)

    tm.add_action(2, [blank,blank,blank], [0], [nowrite, nowrite, nowrite], [0], ['-','-','-'], 'h')
    tm.add_action(2, [blank,blank,blank], [1], [nowrite, nowrite, 1], [0], ['-','-','-'], 'h')

    tm.init()
    tm.run() 
  
    print(tape3)
