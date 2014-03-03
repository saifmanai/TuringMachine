class MiniTuring:
    def __init__(self):
        self.tape_one = [1,1,1]
        self.tape_two = [1,1,0]
        self.sum_tape = []
        self.stack = []
        self.pos1 = 0
        self.pos2 = 0
        self.pos3 = 0
        self.counter = 0
        

        self.pos(2,2)
        self.add(self.pos1,self.pos2)
        self.pos(1,1)
        self.add(self.pos1,self.pos2)
        self.pos(0,0)
        self.add(self.pos1,self.pos2)
        self.show_result()


    def show_result(self):
            
        self.sum_tape.reverse()
        print self.sum_tape

            
    def pos(self,x,y):
        self.pos1 = self.tape_one[x]
        self.pos2 = self.tape_two[y]
        print "Position on tape 1: " + str(x)
        print "Position on tape 2: " + str(y)
        print "Tape 1 position value : " + str(self.pos1)
        print "Tape 2 position value : " + str(self.pos2)
            
    def add(self,pos1,pos2):
        if self.pos1==self.pos2==1 :
            print "Both 1"
            
            if self.counter == 0:
                if self.pos1==1 and self.pos2==0 :
                    self.sum_tape += [self.stack.pop()]
                self.sum_tape += [0]
                self.stack.append(1)
                self.counter = 1

            elif self.counter == 1:
                self.sum_tape += [self.stack.pop()] + [1]
                self.counter == 0
           

        elif self.pos1==self.pos2==0 :
            print "Both 0"
            self.sum_tape += [0]

        elif self.pos1==1 and self.pos2==0 :
            print "a=1 b=0"
            self.sum_tape += [1]

        elif self.pos1==0 and self.pos2==1 :
            print "a=0 b=1"
            self.sum_tape += [1]
        


cv=MiniTuring()
