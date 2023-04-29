
# Emini python parser

## Currently parsing

* Statements: Letting, letting for domains, find, such that.
* Domains: Int, tuples, relation
* Arithmetic and logical expressions
* Quantifiers: forAll, exists
* Concatenation

Returns:

* AST as Networkx attributed tree
* Tree of Nodes
* Tree pretty printed with info about statements

## TODO 27-04-2023

* ~~Parse tuples with a single item in member expression~~
* Unitary operation ( minus and negation)
* ~~Add proper test log files~~
* AST-> Json
* Add normalisers that sort branches in trees
* Parse GIVEN + Where statements
* ~~Handle comments in file~~
* Parse minisation/maximisation
* AST-> Essence
* Improve class names for nodes

Further desiderata

* list comprehension
* exponentials
* Improve error messages
