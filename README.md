# REE: Rewriting Essence Expressions

This is a project to rewrite Essence specs at a class level.
Our focus is high level rewriting which is not currently part of Conjure.
The aim is to create a framework of rewriting components to which machine learning can be applied to determine good heuristics for choosing which rewrites to apply.
The initial criterion to decide goodness is performance, although interpretability and verifiability might also be later criteria.

At an abstract level an Essence spec is a structured abstract syntax tree, and the project rewrites such ASTs, so we are engaged in tree rewriting.
On a practical level we are creating Python modules for a rewriting system, or to interface with existing rewriting systems, and instrumentation for machine learning experiments using parameter tuning, bandits, or generic function approximation schemes such as random forests and neural networks.

Noteworthy components:

* ``astize`` creates a JSON AST from an Essence spec by invoking Conjure

