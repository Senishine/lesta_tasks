# 3. На языке Python реализовать функцию, которая быстрее всего (по процессорным тикам)
# отсортирует данный ей массив чисел. Массив может быть любого размера со случайным порядком чисел
# (в том числе и отсортированным). Объяснить почему вы считаете, что функция соответствует заданным критериям.

# Функция ниже является реализацией алгоритма Tim sort. Несмотря на то, что данный алгоритм более требователен
# по памяти, чем quicksort, в большинстве случаев он является более быстрым алгоритмом
# Данный алгоритм применяет сортировку вставками для небольших по размеру подмассивов и несмотря на то, что
# сортировка вставками имеет худшую ассимптотическую сложность, чем quicksort, на практике для массивов небольшой
# длины она работает лучше. Tim sort имеет большое преимущество для отсортированных или частично упорядоченных списков
# Для примера, ниже, приведены результаты замеров двух алгоритмов сортировок
# timsort time: 0.0707205
# qsort time: 0.5179741
#
# timsort time sorted: 0.06315900000000008
# qsort time sorted: 0.5080302
#
# timsort time reversed: 0.06326699999999996
# qsort time reversed: 0.47533959999999986
import random
import timeit


def calc_min_run(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r


def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])

    i, j, k = 0, 0, l

    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    # оставшиеся элементы из левого списка
    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1
    # оставшиеся элементы из правого списка
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1


def tim_sort(arr):
    n = len(arr)
    min_run = calc_min_run(n)

    # сортировка вставкой отдельных частей массива
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size


def qsort(source):
    if not source:
        return []
    pivot = source[0]
    lesser = qsort([x for x in source[1:] if x < pivot])
    greater = qsort([x for x in source[1:] if x >= pivot])
    return lesser + [pivot] + greater


# Driver program to test above function
if __name__ == "__main__":
    arr = [random.randint(1, 1000_000) for _ in range(1, 100)]
    arr_sorted = [i for i in range(1, 100)]
    arr_reversed = [100 - i for i in range(1, 100)]

    print(f"timsort time: {timeit.timeit(lambda: timSort(arr), number=1000)}")
    print(f"qsort time: {timeit.timeit(lambda: qsort(arr), number=1000)}")

    print(f"timsort time sorted: {timeit.timeit(lambda: timSort(arr), number=1000)}")
    print(f"qsort time sorted: {timeit.timeit(lambda: qsort(arr), number=1000)}")

    print(f"timsort time reversed: {timeit.timeit(lambda: timSort(arr), number=1000)}")
    print(f"qsort time reversed: {timeit.timeit(lambda: qsort(arr), number=1000)}")
