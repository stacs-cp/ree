
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
* AST -> Essence via icing functions

Known missing features:

* no type checking
* in some places variables can be accepted even if not declared

## TODO 14-05-2023

* Add normalisers that sort branches in trees
* Depth measures (depth map)
* Parse GIVEN + Where statements
* Parse minimisation/maximisation
* Automate testing of essence specs generated via icing through conjure
* Deal with "language" token
* Refactor parsing of ":" and "in" in quantifications


Further desiderata

* exponentials
* Improve error messages
