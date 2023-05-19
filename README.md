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

- ``harness`` make AST, GP2, and PDF representation from Essence files
- ``emini.md`` description of EMini fragment of Essence
- ``emini.bnf`` BNF description of EMini
- ``eminipyparser/`` a Python parser for EMini
- ``tests/`` Essence snippets for testing
- ``astize`` creates a JSON AST from an Essence spec by invoking Conjure


## Prerequisites

`harness` needs the following software to be installed:
- [networkx](https://networkx.org/) (install via pip); version 3.1 is known to work
- [graphviz](https://gitlab.com/graphviz/graphviz.git) for graph drawing, or install via brew
- the [GP 2](https://github.com/UoYCS-plasma/GP2) graph rewriting tool
- GP 2 needs the [Judy](https://sourceforge.net/projects/judy/) library


### Notes on building

Graphviz can be difficult to install, so the graph layout code can be tweaked to avoid using the `dot` tool.
This might become an option or something that is auto-detected.

To build Judy on Windows or using XCode, look at the legacy build system `judy-1.0.5/src/sh_build` which simply runs the compiler and creates a library.
This script would be easy to turn into a project file.
On MacOS 12 `sh_build` can be used to build the library, although the shipped `configure` build system also works and will install man pages as well.
(However, the automake files appear to be incompatible with recent versions of automake, so avoid regenerating the makefiles and the configure script.)

