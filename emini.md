# EMini: a miniscule fragment of Essence
## András Salamon and Chris Stone
### 20230302

We propose studying (and implementing a parser for) a small fragment of Essence, which we call EMini.
This is similar to the fragment $E_{FO}$ which is studied by Mitchell and Ternovska 2007.

The `given` part consists of a sequence of statements of the form
```
given D : int(a..b)
```
or
```
given f : function D -> E
```
where `D` and `E` are functions 

