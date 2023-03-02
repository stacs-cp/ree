# EMini: a miniscule fragment of Essence
## András Salamon and Chris Stone
### 20230302

# Introduction

We propose studying (and implementing a parser for) a small fragment of Essence, which we call EMini.
This is similar to the fragment $E_{FO}$ which is studied by Mitchell and Ternovska 2007.


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
where `D`, `E`, and `F` are integer domains declared as `letting`, where the list of domains contains at least one element and the elements are separated by `*`.


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

