# Official Roadmap
## Unit Test
- [ ] Split the unit tests in more file/class
    - [x] core/objects
    - [ ] core/operations
        - [ ] init
        - [ ] memory
        - [ ] math
        - [ ] special
        - [ ] compare
        - [ ] controlflow
    - [ ] commands/memory
    - [ ] commands/operators
    - [ ] commands/controlflow
    - [ ] compiletools
    - [x] Final Tests
        - [ ] New final tests
- [ ] Write more complete test case
- [ ] Test for the cleanness of the registries
## Build & Deploy
- [ ] Port `dist.bat` in a `dist.py` script for build and deploy automation
- [ ] Full automate deploy with an automatic check of the unittests
- [x] Make the project avaiable under Python 3.6
- [x] Check the project with Python 2 (incompatible)
## Documentation
- [ ] **WRITE IT**
    - [ ] commands/operators/eq
    - [ ] commands/operators/neq
    - [ ] others....
- [ ] Translate all the doc from Italian to English
- [ ] New README.md
## New Features
- [ ] For/While loops
- [ ] Subroutine support
- [x] Nested OperatorOperation
    - [ ] Activate it in Commands
- [ ] Support to comparison operation
    - [ ] Greater
        - [ ] GreaterOp
        - [ ] GR command
## Upgrading the MurPy
- [ ] Shift the Environment/Operation interaction to Env's methods
- [ ] Subroutine Support
    - [ ] Multiple subroutine support for Parser
    - [ ] Support for Precompiler
    - [ ] Support for Compiler
- [ ] Write a new BrainFuckVirtualMachine (`BFVM.py`)
    - [ ] With byte and tape options
    - [ ] Choose between C++ and Cython (or even C is good)
    - [ ] With Special Registry at negative positions
    - [ ] Check code validity before run
- [ ] MemObj4Operations Update
    - [ ] Move every part of the Operations to the pure use of MemObj
    - [ ] Move every Command to do it the conversion of the user args to MemObjs instead.
- [ ] Environment Update
    - [ ] Static method for registry clean
    - [ ] Method for adding stack variable
    - [ ] Environment is used for equality and other operation between MemObj
        - [ ] Use this for remove the hazard of duplicated MemObjs
## Bugfixes and general improvements
- [ ] Assert the World
- [x] Move some code from OperatorOperation child's GetCode to his
## Future Additions
- [ ] External language compilation with Parser
- [ ] Type System
    - [ ] Support to multiple cell variable
- [ ] Precompilation Flags
- [ ] Compilation Flags
- [ ] Math operator compile different code with different precomp and comp Flags
- [ ] Dynamic memory operation (HEAP support)
