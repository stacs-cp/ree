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

- ``tests/`` Essence snippets for testing

In ``greee``:
- ``EFormatConverters.py`` convert between EMini and other formats
- ``trans.py`` UI for conversion between formats
- ``harness`` (old) make AST, GP2, and PDF representation from Essence files
- ``astize`` (old) creates a JSON AST from an Essence spec by invoking Conjure

In ``emini``:
- ``emini.md`` description of EMini fragment of Essence
- ``emini.bnf`` BNF description of EMini

## Prerequisites

`harness` needs the following software to be installed:
- [networkx](https://networkx.org/) (install via pip); version 3.1 is known to work
- [graphviz](https://gitlab.com/graphviz/graphviz.git) for graph drawing, or install via brew
- the [GP 2](https://github.com/UoYCS-plasma/GP2) graph rewriting tool
- GP 2 needs the [Judy](https://sourceforge.net/projects/judy/) library

See `greee/README.md` for notes on building.


### List of transformations

We currently consider the following kinds of transformations.
1. Swap the operands of a symmetric binary relation (or commutative binary operation).
1. De Morgan rules for logical expressions.
1. Lex ordering of constraints.

We also need to look at:
1. Distributivity.
1. Reordering of bracketing for associative operations.

