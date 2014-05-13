
"""
This file is a list of definitions for all the turing programs
used for our machine's GUI.
"""

from tm import TuringProgram

plist = list()


program = TuringProgram("Inversion")
program.set_tapes(list("101001"))
program.state_initial = 'invert'
program.set_actions("""\
invert 0 1 > invert
invert 1 0 > invert
invert _ _ - halt""")
plist.append(program)


program = TuringProgram("Palindrome")
program.set_tapes(list("101101"), [])
program.state_initial = 'copy'
program.set_actions("""\
copy   0,_  0,0  >,> copy
copy   1,_  1,1  >,> copy
copy   _,_  _,_  <,- return
return 0,_  0,_  <,- return
return 1,_  1,_  <,- return
return _,_  _,_  >,< test
test   0,0  0,0  >,< test
test   1,1  1,1  >,< test
test   _,_  _,_  -,- halt""")
plist.append(program)


program = TuringProgram("Addition")
program.set_tapes(list("101001"), list("101101"), [])
program.state_initial = 'move'
program.set_actions("""\
move   0,0,_  0,0,_  >,>,> move
move   0,1,_  0,1,_  >,>,> move
move   0,_,_  0,_,_  >,-,> move
move   1,0,_  1,0,_  >,>,> move
move   1,1,_  1,1,_  >,>,> move
move   1,_,_  1,_,_  >,-,> move
move   _,0,_  _,0,_  -,>,> move
move   _,1,_  _,1,_  -,>,> move
move   _,_,_  _,_,_  <,<,< add
add    0,0,_  0,0,0  <,<,< add
add    0,1,_  0,1,1  <,<,< add
add    0,_,_  0,_,0  <,-,< add
add    1,0,_  1,0,1  <,<,< add
add    1,1,_  1,1,0  <,<,< carry
add    1,_,_  1,_,1  <,-,< add
add    _,0,_  _,0,0  -,<,< add
add    _,1,_  _,1,1  -,<,< add
add    _,_,_  _,_,_  -,-,- halt
carry  0,0,_  0,0,1  <,<,< add
carry  0,1,_  0,1,0  <,<,< carry
carry  0,_,_  0,_,1  <,-,< add
carry  1,0,_  1,0,0  <,<,< carry
carry  1,1,_  1,1,1  <,<,< carry
carry  1,_,_  1,_,0  <,-,< carry
carry  _,0,_  _,0,1  -,<,< add
carry  _,1,_  _,1,0  -,<,< carry
carry  _,_,_  _,_,1  -,-,- halt""")
plist.append(program)
