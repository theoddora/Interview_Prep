from collections import deque

# Queue
queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
print(queue)

queue.popleft()
queue.popleft()
print(queue)

queue.appendleft(4)
print(queue)

queue.pop()
print(queue)