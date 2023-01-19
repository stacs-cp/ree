# Rewriting survey
## András Salamon
### 20230116

This document surveys the landscape of practical rewriting systems and part of the prior work on graph and term rewriting, higher-order rewriting, and similar notions as these might apply to rewriting Essence specifications.

The idea is to apply rewriting to an abstract syntax tree obtained from Conjure, feeding the rewritten AST back into Conjure to obtain feedback about performance.
Oz has said that Conjure requires the AST to be perfect so the semantics have to be adhered to very carefully.
It might therefore take some effort to ensure the rewritten AST will always be accepted by Conjure.

[HOPS](http://www.cas.mcmaster.ca/~kahl/HOPS/) is a program development/transformation environment written in OCaml, using term graphs as the basic UI element.
The design seems intended for interactive software development, not for rewriting as a process to be triggered externally.

[Term Graph Rewriting](https://repository.ubn.ru.nl/bitstream/handle/2066/18699/18699_termgrre.pdf) is a 1998 technical report (also a chapter in the [Handbook of Graph Grammars, Volume 2](https://doi.org/10.1142/4180)) about graph transformations on functional expressions represented as directed acyclic graphs.
"Acyclic term graph rewriting can be seen as a sound implementation of term rewriting".

The big problem with rewriting is that the matching problem is generally hard: deciding where a graph rewrite rule can be applied usually requires unavoidable search across the expression tree.
Would using trees instead of DAGs help here?
For instance, one could abstract the local environment of each vertex in a tree into a high level description, which might make matching easier.

Another potential problem is that most rewriting rules are unlikely to match a given expression tree.
A lot of time could therefore be spent scanning for matches which can never trigger.
Perhaps some preprocessing would allow us to avoid such fruitless scanning.

Term graphs allow multiple pointers to a single shared expression as an optimisation (premature?) or a form of compression.

We probably don't care to enforce strong normalisation (termination) or even the existence of a normal form.
We probably also don't care about confluence (the order of applying rewrites might well matter if we allow unsafe ones, although we probably expect solution-set-preserving or at least equivalence-preserving rewrites to be confluent) or the Church-Rosser property (some rewrites might well be non-reversible, so we might end up in different trees which can't be rewritten to each other).

The classic way of seeing rewriting is as a process which makes progress toward some goal, such as a normal form or at least a "simpler" expression.
We don't care about such things.
We just want to rewrite some expression tree to another expression tree in some reasonable way, with the decision as to which rewrite to apply if there is a choice, applied via a separate procedure such as a fixed set of heuristics, the output of a neural network, or a sample from a probability distribution.

A big issue seems to be how to deal with term graphs up to isomorphism: using the isomorphism classes directly leads to a loss of the relationship with specific vertices and edges.
The paper uses standard term graphs which are canonical representatives of the isomorphism classes (I think this requires occasionally relabelling a standard term graph).
Lemma 3.4 is the thing that most rewriting people seem to want, isomorphism checking collapses to equality of the canonical representatives.

