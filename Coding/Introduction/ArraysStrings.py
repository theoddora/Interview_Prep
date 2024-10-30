# Arrays are called lists
# Dynamic arrays by default
arr = [1,2,3]
print(arr)

# Can be used as stacks
arr.append(4)
print(arr)
arr.pop()
print(arr)

arr.insert(10,10)
print(arr)
print(len(arr))

# Initialize an array of size n with default value of 1
n = 5
arr = [1] * n

print(arr)
print(len(arr))

# Sub-lists (aka slicing)
arr = [1,2,3,4,5]
print(arr[1:3])

# Unpacking
a, b, c = [1,2,3]
print(a, b, c)

# Loop through arrays
nums = [1,2,3]

for i in range(len(nums)):
    print("i", nums[i])


# without index
for element in nums:
    print(element)

# with index and value
for i, n in enumerate(nums):
    print("with enumerate", i, n)

# Loop through multiple arrays simultaneously with unpacking
nums1 = [1,3,5]
nums2 = [2,4,6]

for n1, n2 in zip(nums1, nums2):
    # A zip object yielding tuples until an input is exhausted.
    print(n1, n2)

for n1, n2, n3 in zip("abcdefjklop", "hijklmnop", range(199)):
    print(n1, n2, n3)

nums.reverse()
print(nums)

nums.sort(reverse=True)
print(nums)

names = ["alice", "eve", "bob", "eve", "theddy", "danny"]
names.sort(key= lambda x: len(x))

names2 = sorted(names, key= lambda x: (len(x), x))

print(names)
print(names2)

# List comprehension
arr = [i+i for i in range(3)]
print(arr)

# 2D lists
arr = [ [0] *4 for i in range(4)]
print(arr)

# Strings are similar to arrays
s = "abcdefghijklmnop"
print(s[3: 40])

# But they are immutable
s += "a3"
print(s)

# valid numeric strings can be converted
print(int("134") + int("3"))

# valid numbers to string
print(str(123) + str(123))

# Ascii value of char
print(ord('A'))

# Character array
char_array = ['H', 'e', 'l', 'l', 'o']

# Convert to string
string = ''.join(char_array)
print(string)  # Output: "Hello"

string_array = ["Hh", "ee", "llo"]
string = ''.join(string_array)
print(string)