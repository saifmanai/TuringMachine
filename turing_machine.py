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
    def __init__(self, state_initial=0, state_halt='h', symbol_blank='_', dir_left='<', dir_right='>', dir_stay='-'): 
        self.symbol_blank = symbol_blank 
        self.state_initial = state_initial 
        self.state_halt = state_halt 
        self.dir_left = dir_left 
        self.dir_right = dir_right 
        self.dir_stay = dir_stay 
          
        self.tapes = [] 
        self.actions = {} 
      
    def add_tape(self, tape): 
        if not type(tape) is list: raise TuringSetupException("tape is not of type 'list'") 
          
        self.tapes.append(dict(tape=tape, position=0)) 
      
    def add_action(self, state, read_values, write_values, directions, next_state): 
        if not type(read_values) is tuple: raise TuringSetupException("read_values is not of type 'tuple'") 
        for direction in directions: 
            if direction != self.dir_left and direction != self.dir_right and direction != self.dir_stay:  raise TuringSetupException("Invalid direction '%s'" % direction) 
  
        self.actions[(state, read_values)] = dict(write_values=write_values, directions=directions, next_state=next_state) 
      
    def _read(self, tape_entry): 
        return tape_entry['tape'][ tape_entry['position'] ] 
  
    def _write(self, tape_entry, value): 
        tape_entry['tape'][ tape_entry['position'] ] = value 
              
    def _move(self, tape_entry, direction): 
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
  
    def _exec_next_action(self): 
        read_values = [] 
        for tape_entry in self.tapes: 
            read_values.append(self._read(tape_entry)) 
        read_values = tuple(read_values) 
          
        index = (self.state, read_values) 
        if not index in self.actions: raise TuringRuntimeException("No action defined for state '%(state)s' and values '%(values)s'" % dict(state=self.state, values=read_values)) 
          
        action = self.actions[index] 
        for tape_nr, tape_entry in enumerate(self.tapes): 
            self._write(tape_entry, action['write_values'][tape_nr]) 
            self._move(tape_entry, action['directions'][tape_nr]) 
          
        self.state = action['next_state'] 
      
    def run(self): 
        if len(self.tapes) == 0: raise TuringRuntimeException("No tapes defined!") 
        if len(self.actions) == 0: raise TuringRuntimeException("No actions defined!") 
          
        self.state = self.state_initial 
        while self.state != self.state_halt: 
            self._exec_next_action() 
  
  
if __name__ == "__main__": 
    #Exemplu: inversiune 
    tape = [1,0,1,1,0,0] 
    print(tape) 
      
    tm = TuringMachine() 
    tm.add_tape(tape) 
    tm.add_action(0, (0,), (1,), ('>',), 0) 
    tm.add_action(0, (1,), (0,), ('>',), 0) 
    tm.add_action(0, ('_',), ('_',), ('-',), 'h') 
    tm.run() 
  
    print(tape)
