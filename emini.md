# EMini: a miniscule fragment of Essence (v1.0)
## András Salamon and Christopher Stone
### 20230302
Bibtex: emini.bib
Bibliostyle: plainurl.bst

# Introduction

We propose implementing a parser for a small fragment of Essence, which we call EMini.
This is inspired by the fragment $E_{FO}$ which is studied by Mitchell and Ternovska[#MT2008].
Their fragment uses enumerated types and relations, as their work is motivated by computational complexity.
We also use relations but for simplicity we use integer domains instead of enumerated types.
In this note we confine ourselves to defining the fragment and giving a small example of an NP-complete problem, instances of which can be expressed using EMini in a reasonably succinct way.


# The language

An EMini specification consists of three parts.

## Letting

The `letting` part consists of a sequence of statements of the form
```
letting D be domain int(a..b)
```
defining finite integer domains, where `a` and `b` are integer constants,
```
letting R be relation of (D * E * F)
```
where `D` and `E` are integer domains, or
```
letting R be relation((1,2),(1,3))
```
as an example relation.


## Find

The `find` part consists of a sequence of statements of the form
```
find R : relation of (D * E * F)
```
where `D`, `E`, and `F` are integer domains declared as `letting`, the list of domains contains at least one element and is bracketed by parentheses, and the elements in the list are separated by `*`.


## Such that

The `such that` part consists of a sequence of statements of the form
```
such that P
```
where `P` is an expression which is a formula of first-order logic over relations and integers, such that all quantifiers are of the form
```
forAll i : D .
```
or
```
exists i : D .
```
where `D` is an integer domain declared by a `letting` statement.

Expressions may contain `->` (implication), $\verb#/\#$ (logical and), $\verb#\/#$ (logical or), `!` (logical negation), `=` (equality), `!=` (inequality), `<` (less-than), `>` (greater-than), `<=` (less-than-or-equal), `>=` (greater-than-or-equal), and should be bracketed using parentheses to avoid problems with non-associative operators such as `->`.


# Example

The following EMini spec (which is also valid Essence) defines an instance of $\textsc{Graph 3-Colouring}$, where given an input graph the task is to find a mapping of the vertices to 3 colours such that the endpoints of every edge are different.
The vertices are denoted by positive integers.
We use the relation `C` to map a colour to each vertex.
The three constraints require `C` to be a function, which is total, and which is a proper colouring.
```
letting vertices be domain int(1..3)
letting colours be domain int(1..3)
letting G be relation((1,2),(1,3),(2,3))
find C : relation of (vertices * colours)
such that
  forAll (u,c) in C .
     forAll (v,d) in C .
        ((u = v) -> (c = d))
such that
  forAll u : vertices .
     exists c : colours . C(u,c)
such that
  forAll (u,v) in G .
     forAll c,d : colours . (C(u,c) /\ C(v,d) -> (c != d))
```
`conjure solve` returns the following solution:
```
letting C be relation((1, 3), (2, 2), (3, 1))
```

