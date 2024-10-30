empty_dict = {}
print(empty_dict)

filled_dict = {"one": 1, "two": 2, "three": 3}
print(filled_dict)

# Note keys for dictionaries have to be immutable types. This is to ensure that
# the key can be converted to a constant hash value for quick look-ups.
# Immutable types include ints, floats, strings, tuples.
# invalid_dict = {[1,2,3]: "123"}  # => Yield a TypeError: unhashable type: 'list'
valid_dict = {(1, 2, 3): [1, 2, 3]}  # Values can be of any type, however.

print(filled_dict["one"])
print(filled_dict["four"] if "four" in filled_dict else "No")

# From Python 3.5 you can also use the additional unpacking options
var = {"a": 1, **{"b": 2}}  # => {'a': 1, 'b': 2}
print(var)
var2 = {"a": 1, **{"a": 2}}  # => {'a': 2}
print(var2)

# dict comprehension
myMap = { str(i) + "key": i + 1 for i in range(5) }
print(myMap)

# looping through a map
for key in myMap:
     print(key, myMap[key])

for val in myMap.values():
    print(val)

for key, val in myMap.items():
    print(key, val)