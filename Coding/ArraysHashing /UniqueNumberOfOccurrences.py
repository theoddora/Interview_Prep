from collections import defaultdict

class UniqueNumberOfOccurrences:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = defaultdict(int)
        for element in arr:
            d[element] += 1

        uniqueValues = {}
        for values in d.values():
            if values in uniqueValues:
                return False
            else:
                uniqueValues[values] = True

        return True
