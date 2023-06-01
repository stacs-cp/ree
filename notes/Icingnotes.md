# Icing

When going from Abstract Syntax Tree to Essence we need to add some syntactic sugar.

Patterns(bold means the char needs to be added):
letting statements:

- letting *name* **be** *expression*
- letting *name* **be** **domain** *Domain*

Domains:

- int  **( .. )**
- relation  **of**  ( * )
- tuple **( , , , ,)**

Quantifiers:

- forAll *vars* **in** *set*

MemberExpression

- name **( ,  , ,)**

Indexing of tuples

- name **[ ]**

Problem, what procedure puts the parenthesis in an expression only if strictly necessary for operators precedence?
Parenthesis are placed only if the children of an operator node have lower precendence than the node itself. The parenthesis are placed around the children.

Type attributes after transformation??
