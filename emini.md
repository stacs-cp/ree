# EMini: a miniscule fragment of Essence
## András Salamon and Chris Stone
### 20230302

# Introduction

We propose studying (and implementing a parser for) a small fragment of Essence, which we call EMini.
This is similar to the fragment $E_{FO}$ which is studied by Mitchell and Ternovska 2007.


# The language

An EMini specification consists of three parts.

## Given

The `given` part consists of a sequence of statements of the form
```
given D : int(a..b)
```
defining finite integer domains, or
```
given f : function D -> E
```
where `D` and `E` are integer domains.


## Find

The `find` part consists of a sequence of statements of the form
```
find f : function D -> E
```
where `D` and `E` are integer domains declared as `given`.


## Such that

The `such that` part consists of a sequence of statements of the form
```
such that P
```
where `P` is an expression which is a formula of first-order logic over functions and integers, such that all quantifiers are of the form
```
forAll i : D .
```
or
```
exists i : D .
```
where `D` is an integer domain declared as `given`.

