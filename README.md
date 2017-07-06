# MurPy - Brainfuck Transpiler

MurPy is a toolkit and a programming language transpiled in Brainfuck all written in Python 3.
In future MurPy will support multiple routine and a variant of the Object Oriented Programmation.

At now MurPy is in PRE-ALPHA.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

All you need is Python 3.6

### Installing

Simply open a new Python Script (.py) and write a main function with the Code and the right import: 

```
from _environment import Environment  # Compiler
from _interfaceobjects import VAR, SET, ADD, SUB  # Commands used

def main():
    VAR("A", 5)
    VAR("B", 2)
    VAR("C", ADD("A", "B"))
    VAR("D", 2)
```

Write in the "real main" of the script the compile procedure:

```
if __name__ == '__main__':
    env = Environment()
    env.addRoutine(main)
    env.Parse()
    env.Precompile()
    env.Compile()
```

Now you have the code in the property `env.BFCode`. For example put it in a file:

```
    with open('out.bf', 'w') as file:
        file.write(env.BFCode)
```

In the file `demoMurPy.py` there is a demo with a Brainfuck Virtual Machine ready at use.

<!--## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.
-->
## Authors

* **Federico Pasqua** - *Initial work, Design, Coding* - [eisterman](https://github.com/eisterman)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
<!--
## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
-->
