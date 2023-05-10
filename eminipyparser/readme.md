
# Emini python parser

## Currently parsing

* Statements: Letting constant, letting domains, find, such that.
* Domains: bool,int, tuples, relation
* Arithmetic and logical expressions
* Quantifiers: forAll, exists
* Concatenation

Returns:

* AST as Networkx attributed tree
* Tree of Nodes
* Tree pretty printed with info about statements

Known missing features:

* no type checking
* in some places variables can be accepted even if not declared

## TODO 27-04-2023

* ~~Parse tuples with a single item in member expression~~
* ~~Unitary operation ( minus and negation)~~
* ~~Add proper test log files~~
* ~~AST-> Json~~ (via networkx)
* Add normalisers that sort branches in trees
* Parse GIVEN + Where statements
* ~~Handle comments in file~~
* Parse minisation/maximisation
* AST-> Essence
* ~~Improve class names for nodes~~

Further desiderata

* list comprehension
* exponentials
* Improve error messages
