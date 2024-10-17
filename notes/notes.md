# Working notes about REE/greee
## András Salamon and Christopher Stone
### 2023--2024

# 20230327

The Essence parser is coming along, it is still a rough prototype.
Currently we parse:
letting and find. Both constants and domains (named and implicit) for:
- int
- tuples
- relations

Named domains are stored in a dictionary. This means that at this point in time named domains have to be declared before using them, but it could be changed easily.
There is no type-checking. 

Arithmetic expressions and inequalities with operator precedence seem to work correctly.
Next in-line features (taken care by Chris):
- Quantifiers: forAll and exists
- Expression concatenation with " . "


After some brainstorming, we decided to boil down the structure of the Abstract Syntax Tree to its minimal normalised structure. At the moment, due to the way we construct the graph, it may turn into an Abstract Syntax Graph(DAG) with a bit of syntactic sugar still around. This could cause some complications. One of the reasons is that minimal essential structure will make rewriting rules simpler.

Something that was discussed is how to go back from AST to proper Essence.
There are two candidate approaches:
- Inverse-parsing rules. Each parsing rule basically describes how to add back all the parenthesis, commas and so on. There are many and it will be very verbose, but very easy to write.
- Extra rewriting rules. Basically, in the same way we change the spec we can add all the Essence syntactic sugar in the right places post-model transformation. This operation has already been named "Icing". There is some aesthetic beauty to this approach. Possibly easy?

The above will be decided at the next iteration.

Normalisation rules that will be implemented first:
- Small blob before large blob (via node degree or subtree size)
- Small numbers before large
- Lexicographic (alphabetic `a->z`)
- Equalities before inequalities

Regarding the actual rewriting, the next-in-line test will investigate GP2 (taken care of by Andras), a graph transformation program and language developed in York.
First we will look at basic arithmetic rewriting and De Morgan transformations.

Check with Pete about how SR does normalisation: if we rewrite a+b as b+a will they both end up in the same SR normal form, making our rewrite useless?
What SR normalisation happens?


# 20230403

## Parser

A bug remains in the parser relating to ``))+`` and indexed array elements.


## Replacing icing on expressions

Discussed at length how to deal with "icing" on "raw" ASTs.
The idea is that the "raw" AST contains only the AST which is necessary to preserve semantics, while the "iced" version contains parentheses, whitespace, comments, and other elements needed for human readability.
If we want a Python parser to be usable as a library for other applications, such as a plugin for syntax highlighting or code completion in an IDE, then we need to preserve icing, at least up to some modifications (perhaps one can modify whitespace or remove comments).
One use case would be a pretty printer, which reads an Essence spec, applies some normalisation and Pretty Printing transforms.
One example is parenthesising expressions where one has to apply operator precedence to recover the semantics, but where the precedence rules are not necessarily obvious to a non-expert user of Essence, such as using ``(x = y) -> (expression)`` instead of the equivalent ``x = y -> expression`` to clarify how this should be interpreted by a human reader.

Multiple ways to implement this: new AST node ``paren`` with a single child which is an expression (indicating that the expression should be parenthesised), an additional Boolean node flag indicating "this expression is parenthesised", creating two versions of each operator (one for a parenthesised version, one without parentheses), a special child of an expression node indicating parenthesis status.
Single flags or doubling up operators into two types fail to properly represent redundant parentheses like ``(((expression)))``.
Additional children of expression nodes could also work but this requires counting the number of children to reconstruct the right number of parentheses.

Perhaps the easiest would be the new node type ``paren``.
This would interact well with nodes to capture other icing such as whitespace or comments.

A ``space`` node could capture additional whitespace; multiple such nodes would capture multiple spaces.
The AST without any space nodes could then represent a version of the spec where no spaces were used at all.
Some semantic details remain unclear: it seems quite tricky to work out whether a space is required even after a keyword, for instance ``such that x=0`` requires a space after ``such that`` but ``such that(x=0)`` does not require a space.

A ``comment`` node could capture the start of a comment until the end of a line.
This has the advantage that together with ``space`` and ``paren`` nodes the resulting AST could be used to precisely reconstruct the original spec.


## Rewriting hypothesis

It seems likely that we can focus on raw rewrite rules (those applied to raw ASTs without any icing).
The reason is that we should be able to create modified rewrite rules automatically from raw ones, by applying all possible ways to ice a rewrite rule.
In other words, from
```
    +(a,b) -> +(b,a)
```
we generate the four rules
```
    +(a,b) -> +(b,a)
    +(paren(a),b) -> +(b,paren(a))
    +(a,paren(b)) -> +(paren(b),a)
    +(paren(a),paren(b)) -> +(paren(b),paren(a))
```
although this might blow up if we keep all whitespace as separate nodes per character (maybe use the same idea as comments, where the entire run of whitespace is kept as the label of the node).
It is still reasonable to generate a few hundred rewrite rules from a raw rewrite rule, and this might well not affect performance of rewriting since only one of the four rewrite patterns would match at any position.

This leads to the hypothesis: _translating a set of raw rewrite rules into a larger set of iced rewrite rules can be done efficiently, and this does not significantly affect the performance of the rewriting process_.

This is a testable hypothesis that needs to be tested!

If this hypothesis is right then we should keep the AST decorated so that it can be used to recover the original for pretty-printing or other purposes, and this shouldn't cost too much.
If the hypothesis is wrong then we should only store the raw AST and make it clear to the user that the parser will discard icing so a pretty printer based on it will be lossy.


## Project proposal: teaching small language models small languages via instance generation

András has applied to Meta for access to the Llama weights.
Christopher has looked at using [Google T5](https://github.com/google-research/t5x) which might be a better set of base models.
The idea would be to start with a base language model (perhaps one which hasn't been heavily reinforced to be able to regurgigate Wikipedia facts) and to finetune it on Essence.
The Essence training data would be obtained by an instance generation framework combined with a generator which creates valid ASTs randomly from some distribution.
This approach might help to add support for other niche languages to IDEs for code completion by LLM.
This takes the form of an automated procedure which takes a formal description of the language, uses this description to generate instances, and then uses these instances as ground truth to finetune the language model weights.
The hope would be that for synthetic computer languages even a small LLM with a relatively poor grasp of English would be able to learn the language well, at least for IDE code completion tasks, and due to small size would be continuously trainable using CPU only or limited GPU resources.


## Unrelated questions about deep learning

1. Which activation functions are used in common network architectures?
1. Modified ReLU is one of these, what is it called?
1. Has anyone done a comparison of different activation functions for same architecture?


# 20230417

## Harness

The `harness` Python script now:
1. runs Conjure to parse a spec (and optionally a parameter file),
1. reads the resulting JSON representation of the internal abstract syntax tree (AST), 
1. translates the AST into a GP2-style labelled graph,
1. prints the GP2-style graph.

The current graph representation of the AST is based on the following schema, that is similar to the XML style representation of trees with ordered children.
Every edge is labelled with one of the labels `child`, `firstChild`, or `nextChild`.
A node representing a dictionary is linked to all its elements by `child` edges.
The node representing an entry in a dictionary is labelled with its dictionary key, and linked to the node for its value by a `child` edge.
A parent node representing a list is linked to the first element in the list by a `firstChild` edge, and entries in the list link to the next element by `nextChild` edges.
(There are no links from the parent node of a list to the second and subsequent children.)
Integers and strings are stored.
`None` values are represented as null values.

The semantics of nulls are not clear (what is their purpose?), probably need to check with Oz.

Once the Python parser output is stable it can be integrated into the harness as another way to create the GP2 instance graph.


# 20230511

## rewriting meeting highlights

- Handle parsing of the absolute value operator (this could conflict with list comprehension which will not be parsed yet)
- Lattice navigation, first graph transformation will be semantically invariant
- ModRef paper. potential story: If we have a set of transformation rules, when is it a good time to use them so that they have a positive impact? We must generate lots instances and learn about their effect on them
- Profiling conjure and savile row. Which spec/solver combination affect the translation?
- For the future: How to generate rewrite rules? in particular so that a specific property of the graph is preserved


# 20230612

* Jimmy Lee automated dominance generation
* implied constraints from symmetry breaking
* "exploratory reformulation" as title


# 20230615

GP2 fix reordering of node numbers


# 20230807

Ian's high level view of work for CPAIOR:

1. accept an Emini specification,
2. apply variable introduction, and/or some simple de Morgan style rewrites,
3. test sequences of rewrites against a test set of instances, hopefully at least one sequence works to improve performance.

In PTHG paper we envisaged Monte Carlo tree search to investigate sequences of rewrites.

Adding variables is powerful (as in the Steel Mill paper) because when we add a variable we also add a set of domain values that the variable can take, and this stores information that is updated when values are removed from the domain.
Ian's hypothesis is that this storage of information in the domain of the new variables is why variable introduction allows increasing the power of a proof system (such as resolution versus extended resolution, where the domain of new variables is Boolean and yet is still enough to provably increase the power of the system).

*Hypothesis:* reordering constraints a priori might (through introduction of variables and variable ordering heuristics) affect performance of a model.
Can constraint ordering be ignored (which would allow normalisation), or is it important?

Related issue is renaming of variables: superficially different, ideally want to identify isomorphism via renaming.

If assuming a canonical constraint ordering makes no difference, we could then work with normalised formulas only.



# 20231214

Static rewrites versus dynamic rewrites

The domoverwdeg heuristic is an example of a dynamic rewrite strategy: it applies rewriting of the tree during search, as the domains change.
Class-level rewriting is a static rewrite strategy.


# 20240408

Validate solutions of the rewritten spec by reversing the transformation implemented by the rewriting, and applying this reverse function to the solutions found for the rewritten spec to obtain solutions for the original spec.
In other words: find the inverse functor where the original functor maps the original spec to the rewritten spec, and apply it to the solution.


# 20241017

(From 20240212)
There are two main obstacles.

First, the amount of time it is taking to perform an experiment is so large and also so variable, that it is difficult to detect any difference a rewrite might make to a spec.
Much of this is due to SR needing a JVM to start every time it is run.
If we want meaningful data to guide our MCTS approach then we need to either magnify the effect of each rewriting step somehow (maybe work with quite large instances only?) or make the Conjure/SR/solver toolchain overhead less variable and possibly also much smaller.

[We addressed this in the ICGT 2024 paper by finding problems where the difference was huge: the rewritten spec was feasible where the original spec blew up Savile Row.]

Second, we currently have very few rewrite rules.
Many of the interesting tractable rules are already implemented inside SR and/or Conjure, leaving difficult ones and those with limited applicability.
We need a way to generate more rewrite rules and possibly also to validate them with a theorem prover (or give up on soundness).

[We found some additional rewrite rules, such as Peirce's Law.
This is still work in progress.]

