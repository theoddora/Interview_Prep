#HashSet
mySet = set()
mySet.add(1)
mySet.add(2)
print(mySet)

print(len(mySet))

print(1 in mySet)
print(10 in mySet)
print(10 in {10,12})

mySet.remove(2)
print(mySet )

# list to set
mySetFromList = set([1,23,4,5,6,7,6])
print(mySetFromList)

# set comprehension
mySetUsingComprehension = {i for i in range(2)}
print(mySetUsingComprehension)

# sets in Python are a mutable collection of unordered, unique immutable elements.

A = {1, 2, 4, 6, 8}
B = {1, 2, 3, 4, 5}

# Set union using .union()
print(A.union(B))

# Set union using the | operator
print(A | B)

# Output:
# {1, 2, 3, 4, 5, 6, 8}


A = {1, 2, 4, 6, 8}
B = {1, 2, 3, 4, 5}

# Use the method
print(A.intersection(B))

# Use the & operator
print(A & B)

# Output:
# {1, 2, 4}

A = {1, 2, 4, 6, 8}
B = {1, 2, 3, 4, 5}

# Use the method
print(A.difference(B))

# Use the - operator
print(A - B)

# Output:
# {6, 8}


A = {1, 2, 4, 6, 8}
B = {1, 2, 3, 4, 5}

print(A.symmetric_difference(B))

# Output:
# {3, 5, 6, 8}

A = {1, 2, 3, 4, 5}
B = {1, 2, 4}


print(A.issuperset(B))
# Output: True

print(B.issubset(A))
# Output: True


S1 = {1, 2, 3}
S2 = S1.copy()  # independent copy of S1
S1.clear()

print(S1)
# Output: set()

print(S2)
# Output: {1, 2, 3}

# Initialize a set with a bunch of values.
some_set = {1, 1, 2, 2, 3, 4}  # some_set is now {1, 2, 3, 4}

# Similar to keys of a dictionary, elements of a set have to be immutable.
# invalid_set = {[1], 1}  # => Raises a TypeError: unhashable type: 'list'
valid_set = {(1,), 1}
print("valid set is ", valid_set)

# Add one more item to the set
filled_set = some_set
filled_set.add(5)  # filled_set is now {1, 2, 3, 4, 5}
print("filled set", filled_set)
print("some set", some_set)
# Sets do not have duplicate elements
filled_set.add(5)  # it remains as before {1, 2, 3, 4, 5}
print("filled set", filled_set)

# Do set intersection with &
other_set = {3, 4, 5, 6}
print(filled_set & other_set)  # => {3, 4, 5}

# Do set union with |
print(filled_set | other_set)  # => {1, 2, 3, 4, 5, 6}

# Do set difference with -
print({1, 2, 3, 4} - {2, 3, 5})  # => {1, 4}

# Do set symmetric difference with ^
print({1, 2, 3, 4} ^ {2, 3, 5})  # => {1, 4, 5}

# Check if set on the left is a superset of set on the right
print({1, 2} >= {1, 2, 3} ) # => False

# Check if set on the left is a subset of set on the right
print({1, 2} <= {1, 2, 3})  # => True

# Check for existence in a set with in
2 in filled_set   # => True
10 in filled_set  # => False

# Make a one layer deep copy
filled_set = some_set.copy()  # filled_set is {1, 2, 3, 4, 5}
print(filled_set is some_set )       # => False
print(filled_set == some_set)