
# Emini python parser

## Currently parsing

* Statements: Given, where, letting constant, letting domains, find, such that.
* Domains: bool,int, tuples, relation
* Arithmetic and logical expressions
* Quantifiers: forAll, exists
* Concatenation

Returns:

* AST as Networkx attributed tree
* Tree of Nodes
* Tree pretty printed with info about statements
* AST -> Essence via icing functions
* GP2 Graph

Known missing features:

* no type checking
* in some places variables can be accepted even if not declared

## TODO 10-08-2023

* Add normalisers that sort branches in trees
* Depth measures (depth map)
* Parse minimisation/maximisation
* Deal with "language" token
* Montecarlo tree exploration


Further desiderata

* exponentials
* Improve error messages
