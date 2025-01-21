def myFunc(n, m):
    return n * m


# nested functions have access to outer variables
def outer(a, b):
    c = "c"

    def inner():
        return a + b + c

    return inner()


print(outer("2", "4"))


# can modify objects but not reassign unless using nonlocal keyword
def double(arr, val):
    def helper():
        # Modifying array works
        for i, n in enumerate(arr):
            arr[i] = 2 * arr[i]

        # will only modify val in helper scope
        # val *= 2

        # this will modify val in helper function

        nonlocal val
        val *= 2

    helper()
    print(arr, val)

double([1,2,3,4], 5)

def printRandNumber(num: int):
    print(num)
    print(15 == num)

randNumber = 15.45
printRandNumber(randNumber)
