class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        counter = 0
        ans = [None] * (len(word1) + len(word2))

        ansIndex = 0
        for i, j in zip(word1, word2):
            ans[ansIndex] = i
            ansIndex += 1
            ans[ansIndex] = j
            ansIndex += 1

        while counter < len(word1):
            ans[ansIndex] = word1[counter]
            ansIndex += 1
            counter += 1

        while counter < len(word2):
            ans[ansIndex] = word2[counter]
            ansIndex += 1
            counter += 1

        return ''.join(ans)