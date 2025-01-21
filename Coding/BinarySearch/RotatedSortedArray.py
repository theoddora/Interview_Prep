from typing import List

def find_the_target_in_a_rotated_sorted_array(nums: List[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        print(left, right, mid)
        if nums[mid] == target:
            return mid

        if nums[mid] < target:
            if nums[right] < target:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if mid + 1 < len(nums) and nums[mid] > nums[mid + 1]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

def main():
    print(find_the_target_in_a_rotated_sorted_array([8, 9, 11, 1, 3, 4, 5, 7], 10))

if __name__ == '__main__':
    main()