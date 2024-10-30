# Heap
import heapq

#under the hood they are arrays
minHeap = []
heapq.heappush(minHeap, 2)
heapq.heappush(minHeap, 3)
heapq.heappush(minHeap, 4)
heapq.heappush(minHeap, 1)
heapq.heappush(minHeap, 0)
print(minHeap)

while len(minHeap) > 0:
    print(minHeap)
    print(heapq.heappop(minHeap))

# No max heap by default
# Work around is to use min heap and multiply by -1 when push and pop
maxHeap = []
heapq.heappush(maxHeap, -2)
heapq.heappush(maxHeap, -3)
heapq.heappush(maxHeap, -4)
heapq.heappush(maxHeap, -1)
heapq.heappush(maxHeap, 0)

# max will be at index 0
print(-1 * maxHeap[0])


# if you already have your initial values
arr = [ 2, 1, 8, 4, 5]

# you can do it in linear time with heapify
heapq.heapify(arr)

while arr:
    print(heapq.heappop(arr))