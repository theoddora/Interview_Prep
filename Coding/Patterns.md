# Sliding Window

## Definition
Used when you need to process a series of data elements like list, string. In the sliding-window pattern you find specific things in the list by looking at a smaller part of the list at a time. The part of the list that you are looking at is called a window. This window slides one step at a time untik the entire list is scanned. 

## When to use
If a problem asks you to find a subset of elements that satisfies a given condition, think about sliding windown pattern. Your input would be a linear data structure like an array, string or a linked list. And you would have to find the longest or the shortest substring/subarray that satisfies a particular condition.

## Examples
- Find the longest substring with k unique characters in a given string

# Subset pattern

## Definition
The subset pattern is used when you need to find all the possible combinations of elements from a given set. Repetitions may or may not be allowed depending on the problem. In the subset pattern we need to explore all the possible arrangements of elements from the given set. 

## Examples
- Permutations of elements in array

# Modified Binary Search

## Definition
The core idea of binary search is to divide the search space in half again and again. In the modified Binary Search pattern the idea remains the same but we need to adjust to solve the problem. 

## Example
- Saearch in Rotated sorted array

# Top K Elements

## Definition
The top K elements pattern is used to select K elements from a larger data set given a particular condition. 

##  When to use
Think about this pattern whenever the problem asks you to find top ranking elements from a data set. Input would usually be a linear data structure like an array or a list. 

## Example
- Kth largest element in an array

# Binary Tree DFS

## Definition
Binary tree DFS helps you visit every node on the tree focusing on one branch at a time. Generally you would use recursuion to do this. 

## Examples
- Maximum depth of binary tree

# Topological sort

## Definition
The topological sort is used to arrange elements in a specific order when they have dependencies on each other. It's particularly useful for DAGs. 

## When to use
Think of topological sort whenever you have a prerequisite chain. 

## Example 
- Course schedule

# Binary Tree BFS 

## Definition 
BFS explores all the nodes at the same level in different branches first. To achieve this, we use Queue DS. 

## Example
- level order traversel in binary tree

# Two pointer 

## Definition
Two pointer pattern is useful when you need to iterate through a sorted array. Each pointer will keep a track of an index. By moving the pointers smartly we can often solve the problem in a single pass, making the algorithm more efficient. 

## Example 
- Two sum problem
- Three sum problem