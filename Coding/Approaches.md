# Optimization Problems
1. Greedy Method
2. Dynamic Programming
3. Branch and Bound


## Greedy method

```python
def algorithm_greedy(a, n):
    for i in range(1, n):
        x = select(a)
        if feasible(x):
            solution = solution + x 
```

What are Feasible and Optimal Solutions.