
# pystrector

#### (Py)thon (Str)uct Refl(ector)

#### Small package for displaying core Python structures

```python
strector = Pystrector()
some_object = 1
reflector = strector.bind_object(some_object)
print(reflector.ob_base.python_value.ob_refcnt.python_value)
```


### Git

```shell
git clone https://github.com/bontail/pystrector.git
```

### Python

To download the package enter the command.

```shell
python3 -m pip install pystrector
```