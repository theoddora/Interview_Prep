from typing import List


def getCuttingLength(heights: List[int], option: int) -> int:
    heigthSum = 0
    for height in heights:
        heigthSum += max(0, height - option)
    return heigthSum


def binarySearch(heights: List[int], k: int) -> int:
    left = 0
    right = heights[-1]

    bestSum = float("inf")
    bestHeight = float("inf")

    while left <= right:
        heightOption = (left + right) // 2
        heightSumOutput = getCuttingLength(heights, heightOption)
        print(left, right, heightOption, heightSumOutput)

        if heightSumOutput < bestSum and heightSumOutput >= k:
            bestSum = heightSumOutput
            bestHeight = heightOption
        if heightSumOutput >= k:
            left = heightOption + 1
        else:
            right = heightOption - 1

    return bestHeight


def cutting_wood(heights: List[int], k: int) -> int:
    heights.sort()

    return binarySearch(heights, k)

def main():
    print(cutting_wood([2,3,6,8], 0))

if __name__ == '__main__':
    main()