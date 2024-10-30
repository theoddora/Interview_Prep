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
