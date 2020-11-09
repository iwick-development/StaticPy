# StaticPy
 StaticPy is a interperater/environement that allows you to write Python
 code in a static type format for quicker and less error prone development.

# Code Examples
## Simple Hello World
```python
var message string = "Hello World!"
print(message)

--OUTPUT--
Hello World!

--OUTPUT CODE--
message = "Hello World!"
print(message)
```

## Function Syntax
```python
def int calc():
    return 1 * 2

print(calc)
```

# Allowed Types
## Variables
- string
```
A string type is anything within "" or '' such as "Hello" and 'Hello'
```
- list
```
A list type is a python list such as ["test"]
```
- dict
```
A dict type is a python dict or json such as {'Hello': 'World'}
```
- bool
```
A bool type can be eather True or False (case sensative)
```
- int
```
A int type is any whole number
```
- float
```
A float type is any decimal number such as 10.322
```

## Functions
- string
- list
- dict
- bool
- int
- float
- void
```
 The void type means that StaticPy will ignore the return, and not check for one.
 This also means that it will ignore the type of output if a return does exist.
```
