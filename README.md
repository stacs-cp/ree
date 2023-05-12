# REE: Rewriting Essence Expressions

This is a project to rewrite Essence specs at a class level.
We focus on rewriting rules which are not currently part of Conjure.
The aim is to create a framework of rewriting components to which machine learning can be applied to determine good heuristics for choosing which rewrites to apply.
The initial criterion to decide goodness is performance.
Later we also intend to consider how the rewriting rules could be formally verified, to potentially extend proof verification from just SAT solver backends further up the pipeline.
Interpretability might also be a later criterion.

At an abstract level an Essence spec is a structured abstract syntax tree, and the project rewrites such ASTs, so we are engaged in tree rewriting.
On a practical level we are creating Python modules for a rewriting system, or to interface with existing rewriting systems, and instrumentation for machine learning experiments using parameter tuning, bandits, or generic function approximation schemes such as random forests and neural networks.

Our current approach targets the [GP2](https://github.com/UoYCS-plasma/GP2) graph rewriting system.

Noteworthy components:

* ``harness`` make AST, GP2, and PDF representation from Essence files
* ``emini.md`` description of EMini fragment of Essence
* ``emini.bnf`` BNF description of EMini
* ``eminipyparser/`` a Python parser for EMini
* ``tests/`` Essence snippets for testing
* ``astize`` creates a JSON AST from an Essence spec by invoking Conjure

