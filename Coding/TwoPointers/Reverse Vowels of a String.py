from collections import deque

class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        stack = deque()

        for char in s:
            if char in vowels:
                stack.append(char)

        stringToReturn = ""
        for char in s:
            if char in vowels:
                stringToReturn += stack.pop()
            else:
                stringToReturn += char
        return stringToReturn