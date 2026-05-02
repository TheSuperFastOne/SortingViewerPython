def bubbleSort(daList):
    n = len(daList.data)

    while n > 1:
        swapped = False
        last_swap = 0
        a = daList.read(0)

        for j in range(n - 1):
            b = daList.read(j + 1)

            if a > b:
                daList.write(j, b)
                daList.write(j + 1, a)
                swapped = True
                last_swap = j + 1
            else:
                a = b

        if not swapped:
            break

        n = last_swap


def shaker(daList):
    left = 0
    right = len(daList.data) - 1

    while left < right:
        swapped = False

        # Bubble largest item to the right.
        for j in range(left, right):
            if daList.read(j) > daList.read(j + 1):
                daList.swap(j, j + 1)
                swapped = True

        right -= 1

        if not swapped:
            break

        swapped = False

        # Bubble smallest item to the left.
        for j in range(right, left, -1):
            if daList.read(j - 1) > daList.read(j):
                daList.swap(j - 1, j)
                swapped = True

        left += 1

        if not swapped:
            break
