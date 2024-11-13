# Linear

## Two pointer 

### Definition
Two pointer pattern is useful when you need to iterate through a sorted array. Each pointer will keep a track of an index. By moving the pointers smartly we can often solve the problem in a single pass, making the algorithm more efficient. 

It allows you to significantly reduce the time complexity of problems that involve traversing a linear structure. 
Instead of Brute force approach where you might check every combination of elements which could lead to O(n^2) complecity, two pointers often allow you to solve this problems in a linear time O(n) making it incredibly efficient. There are two main methods of using two pointers:
- Same direction : processing or scanning the data in a single pass - fast and slow pointer approach for detecting cycles in linked lists or for finding the middle of the list. 
- Opposite direction : problems for finding pairs or comparing elements from opposite end of a data structure i.e. 2Sum. 
 
Each are used for different types of problems.  

### Example 
- Two sum problem - Find two numbers in a sorted array that add up to a given target.
- Three sum problem
- Palindrome Check: Check if a given string is a palindrome by comparing characters from both ends.

### All sub-patterns of two-pointers:
https://www.youtube.com/watch?v=4EDiy-jbPaE

#### Approaching pointers
**Pattern**: Start with two pointers: one at the beginning of the array (or string) and the other at the end. Move them towards each other based on certain conditions until they meet.

Two Sum (Sorted Array) example
```python
def two_sum(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None
```

#### Same Direction
Pattern: Divide the problem in half and use two pointers to solve each half independently, then combine the results.


#### Fast and slow pointers
 
####  Separate pointers

## Sliding Window

### Definition
Used when you need to process a series of data elements like list, string. In the sliding-window pattern you find specific things in the list by looking at a smaller part of the list at a time. The part of the list that you are looking at is called a window. This window slides one step at a time untik the entire list is scanned.  

This is an extension of the two pointer pattern but with a more focused purpose. Sliding window refines it by making a window of elements within the data dynamically adjusting its size as you progress through the structure. As you progress through the structure, essentially you are using two pointers but the goal is to manage a range or subset of elements that satisfy a specific condition like a subarray.    

### When to use
If a problem asks you to find a subset of elements that satisfies a given condition, think about sliding windown pattern. Your input would be a linear data structure like an array, string or a linked list. And you would have to find the longest or the shortest substring/subarray that satisfies a particular condition.

### Examples
- Find the longest substring with k unique characters in a given string

## Modified Binary Search

### Definition
The core idea of binary search is to divide the search space in half again and again. In the modified Binary Search pattern the idea remains the same but we need to adjust to solve the problem. 

### Example
- Saearch in Rotated sorted array

## Subset pattern

### Definition
The subset pattern is used when you need to find all the possible combinations of elements from a given set. Repetitions may or may not be allowed depending on the problem. In the subset pattern we need to explore all the possible arrangements of elements from the given set. 

### Examples
- Permutations of elements in array

# Non-Linear

## Binary Tree BFS 

### Definition 
BFS explores all the nodes at the same level in different branches first. To achieve this, we use Queue DS. 

### Example
- level order traversel in binary tree
- Find shortest path

## Binary Tree DFS

### Definition
Binary tree DFS helps you visit every node on the tree focusing on one branch at a time. Generally you would use recursuion to do this. In DFS we use Stack. Most often, the stack DFS uses is the call stack. 

## Examples
- Maximum depth of binary tree
- Exmplore all paths 
- Num of islands

## Topological sort

### Definition
The topological sort is used to arrange elements in a specific order when they have dependencies on each other. It's particularly useful for DAGs. 

### When to use
Think of topological sort whenever you have a prerequisite chain. 

### Example 
- Course schedule

## Backtracking
Extension of DFS. In DFS we typically traverse a pre-built structure like a tree or graph where the nodes and connections are already defined. With backtracking you often have to build the solution yourself and explore different options.

### Example 
- Combinatorial problems  

## Priority Queue - Heap

### Definition
The top K elements pattern is used to select K elements from a larger data set given a particular condition. 

### When to use
Think about this pattern whenever the problem asks you to find top ranking elements from a data set. Input would usually be a linear data structure like an array or a list. 

### Example
- Kth largest element in an array

## Dynamic programming
Optimizing a solution by breaking it down to overlapping sub-problems. Two ways:
- Top down - backtracking with memoization
- Bottom up 