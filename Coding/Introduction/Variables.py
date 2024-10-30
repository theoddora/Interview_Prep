# Variables are dynamically typed
# types are determined at runtime
n = 0
print("n = ", n)

n = "abc"
print("n = ", n)

n, m = 0, "abc"

#Incrementing
n = n + 1
print("n = ", n)

n += 1
print("n = ", n)

# None is null (absence of value)
a = None
print("a = ", a)

# If statements don't need parentheses
if a is None:
    print("a is None")
elif n == 2:
    print("a is 2")
else:
    print("a is not 2")

# and is &&
# or is ||

#while loops
n = 0
while n < 0:
    print("n = ", n)
    n = n + 1

# for loops
for i in range(0):
    print("i = ", i)

for j in range(1, 2):
    print("j = ", j)

for i in range(4, 2, -1):
    print("i = ", i)

# Division is decimal by default
print(5 / 2 )

# Double slash rounds down (integer division)
print(5 // 2)

# Careful: most languages round towards 0 by default so negative number would round down
print(-3 // 2)

# A workaround for rounding towards zero is to use decimal division and then convert to int
print(int(-3/2))

# Modulo is similar to most languages
print(10 % 3)

print(-10 % 3)

# to be consistent with other languages modulo
import math
print(math.fmod(-10, 3))

print(math.floor(3.14))

print(math.ceil(3.14))

print(math.sqrt(9))

print(math.pow(2,3))

# Max/Min integer
print( float("inf"))
print(float("-inf"))

# python numbers are infinite, they never overflow
