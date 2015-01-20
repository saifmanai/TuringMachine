
"""
File: programs.py
A list of example programs, used for our machine's GUI.
"""

"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from tm import TuringProgram

plist = list()


"""
Inversion
This program simply inverts all digits in the inserted binary number.
"""
program = TuringProgram("Inversion")
program.set_tapes(list("101001"))
program.state_initial = 'invert'
program.set_actions("""\
invert 0 1 > invert
invert 1 0 > invert
invert _ _ - halt""")
plist.append(program)



"""
Palindrome Checker
It uses 2 tapes: the first one is for the binary number that needs to be checked.
The second one is used as a temporary storage and should be empty when running the program.
The value inserted in the first tape is copied to the second one.
Then, both tapes are checked for equality, but from opposite ends.
If the value is a palindrome, the program will simply end.
If it's not a plaindrome, the program will throw an error.
"""
program = TuringProgram("Palindrome Checker")
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



"""
Addition
This program uses 3 tapes: 2 for the input values (as binary numbers),
and the last one for the result (this one should be empty when running the program).
The program moves to the right start of each value, and then adds each digit.
The carry is stored using a separate state.
"""
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



program = TuringProgram("Multiplication")
program.set_tapes(list("1011"), list("1110"), [])
program.state_initial = 'move'
program.set_actions("""\
move         0,0,_  0,0,_  >,>,> move
move         0,1,_  0,1,_  >,>,> move
move         0,_,_  0,_,_  >,-,> move
move         1,0,_  1,0,_  >,>,> move
move         1,1,_  1,1,_  >,>,> move
move         1,_,_  1,_,_  >,-,> move
move         _,0,_  _,0,_  -,>,> move
move         _,1,_  _,1,_  -,>,> move
move         _,_,_  _,_,_  <,<,< multi
multi        0,0,_  0,0,0  <,-,< multi
multi        0,0,0  0,0,0  <,-,< multi
multi        0,0,1  0,0,0  <,-,< multi
multi        0,1,_  0,1,0  <,-,< multi
multi        0,1,0  0,1,0  <,-,< multi
multi        0,1,1  0,1,0  <,-,< multi
multi        1,0,_  1,0,0  <,-,< multi
multi        1,0,0  1,0,0  <,-,< multi
multi        1,0,1  1,0,0  <,-,< multi
multi        1,1,_  1,1,1  <,-,< multi
multi        1,1,0  1,1,1  <,-,< multi
multi        1,1,1  1,1,0  <,-,< multi-carry
multi        _,0,_  _,0,_  >,<,- multi-shift
multi        _,0,0  _,0,0  >,<,- multi-shift
multi        _,0,1  _,0,1  >,<,- multi-shift
multi        _,1,_  _,1,_  >,<,- multi-shift
multi        _,1,0  _,1,0  >,<,- multi-shift
multi        _,1,1  _,1,1  >,<,- multi-shift
multi        _,_,_  _,_,_  -,-,- halt
multi        _,_,0  _,_,0  -,-,- halt
multi        _,_,1  _,_,1  -,-,- halt
multi-carry  0,0,_  0,0,1  <,-,< multi
multi-carry  0,0,0  0,0,1  <,-,< multi
multi-carry  0,0,1  0,0,0  <,-,< multi-carry
multi-carry  0,1,_  0,1,1  <,-,< multi
multi-carry  0,1,0  0,1,1  <,-,< multi
multi-carry  0,1,1  0,1,0  <,-,< multi-carry
multi-carry  1,0,_  1,0,1  <,-,< multi
multi-carry  1,0,0  1,0,1  <,-,< multi
multi-carry  1,0,1  1,0,0  <,-,< multi-carry
multi-carry  1,1,_  1,1,0  <,-,< multi-carry
multi-carry  1,1,0  1,1,0  <,-,< multi-carry
multi-carry  1,1,1  1,1,1  <,-,< multi-carry
multi-carry  _,0,_  _,0,1  >,<,- multi-shift
multi-carry  _,0,0  _,0,1  >,<,- multi-shift
multi-carry  _,0,1  _,0,0  -,-,< multi-carry
multi-carry  _,1,_  _,1,1  >,<,- multi-shift
multi-carry  _,1,0  _,1,1  >,<,- multi-shift
multi-carry  _,1,1  _,1,0  -,-,< multi-carry
multi-carry  _,_,_  _,_,1  -,-,- halt
multi-carry  _,_,0  _,_,1  -,-,- halt
multi-carry  _,_,1  _,_,0  -,-,< multi-carry
multi-shift  0,0,0  0,0,0  >,-,> multi-shift
multi-shift  0,0,1  0,0,1  >,-,> multi-shift
multi-shift  0,0,_  0,0,_  >,-,> multi-shift
multi-shift  0,1,0  0,1,0  >,-,> multi-shift
multi-shift  0,1,1  0,1,1  >,-,> multi-shift
multi-shift  0,1,_  0,1,_  >,-,> multi-shift
multi-shift  1,0,0  1,0,0  >,-,> multi-shift
multi-shift  1,0,1  1,0,1  >,-,> multi-shift
multi-shift  1,0,_  1,0,_  >,-,> multi-shift
multi-shift  1,1,0  1,1,0  >,-,> multi-shift
multi-shift  1,1,1  1,1,1  >,-,> multi-shift
multi-shift  1,1,_  1,1,_  >,-,> multi-shift
multi-shift  _,0,0  _,0,0  <,-,< multi
multi-shift  _,0,1  _,0,1  <,-,< multi
multi-shift  _,0,_  _,0,_  <,-,< multi
multi-shift  _,1,0  _,1,0  <,-,< multi
multi-shift  _,1,1  _,1,1  <,-,< multi
multi-shift  _,1,_  _,1,_  <,-,< multi
multi-shift  0,_,0  0,_,0  -,-,- halt
multi-shift  0,_,1  0,_,1  -,-,- halt
multi-shift  1,_,0  1,_,0  -,-,- halt
multi-shift  1,_,1  1,_,1  -,-,- halt""")
plist.append(program)
