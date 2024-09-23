# REE: Rewriting Essence Expressions

This Python module includes a parser for the Emini subset of the Essence constraint programming language, as well as supporting infrastructure to translate the AST to and from other formats such as GP2, networkx, and the JSON format of Conjure.


## Emini python parser

### Currently parsing

* Statements: Given, where, letting constant, letting domains, find, such that.
* Domains: bool,int, tuples, relation
* Arithmetic and logical expressions
* Quantifiers: forAll, exists
* Concatenation

### Returns:

* AST as Networkx attributed tree
* Tree of Nodes
* Tree pretty printed with info about statements
* AST -> Essence via icing functions
* GP2 Graph

## Known missing features:

* no type checking
* in some places variables can be accepted even if not declared

## TODO 10-08-2023

* Add normalisers that sort branches in trees
* Depth measures (depth map)
* Parse minimisation/maximisation
* Deal with "language" token
* Montecarlo tree exploration


## Further desiderata

* exponentials
* Improve error messages


## Prerequisites

The following software first needs to be installed:
- [networkx](https://networkx.org/) (install via pip); version 3.1 is known to work
- [graphviz](https://gitlab.com/graphviz/graphviz.git) for graph drawing, or install via brew
- the [GP 2](https://github.com/UoYCS-plasma/GP2) graph rewriting tool
- GP 2 needs the [Judy](https://sourceforge.net/projects/judy/) library

In ``bin``:
- ``emini2gp2.py`` convert from EMini to GP2
- ``gp22emini.py`` convert from GP2 to EMini
- ``gp22json.py`` convert from GP2 to JSON
- ``harness`` make AST, GP2, and PDF representation from Essence or EMini
- ``trans`` translate from input to output format (e.g. AST,GP2,Emini,Json)


### Notes on building

Graphviz can be difficult to install, so the graph layout code can be tweaked to avoid using the `dot` tool.
This might become an option or something that is auto-detected.

To build Judy on Windows or using XCode, look at the legacy build system `judy-1.0.5/src/sh_build` which simply runs the compiler and creates a library.
This script would be easy to turn into a project file.
On MacOS 12 `sh_build` can be used to build the library, although the shipped `configure` build system also works and will install man pages as well.
(However, the automake files appear to be incompatible with some recent versions of automake, so be careful if regenerating the makefiles and the configure script.)

To create the `greee` package, we use `setuptools`: `python3 -m build` creates the package in `dist`.
The documentation in `docs` is built using `make html` and requires Sphinx to be installed (`brew install sphinx-doc` or follow the Sphinx official documentation).

