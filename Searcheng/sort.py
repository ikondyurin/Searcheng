"""This module contains sorting method"""

def do_sort(array):
    """Sorts the elements of the array of arrays.

    Args:
    array: array of arrays

    Yields
    elements of array, sorted
    """
    first_elements = []
    iter_array = []
    
    for i, s in enumerate(array): #we now turn arrays into iterators
        s = iter(s)
        iter_array.append(s)
        first_elements.append(next(s))
    print(first_elements)
    
    while True:
        try:
            minimal = min(first_elements)
        except ValueError:
            break
        index = first_elements.index(minimal)
        yield minimal
        try:
            first_elements[index] = next(iter_array[index])
            #we go to the next element in iterator
            """
 #           minimal = next(iter_array[first_elements.index(minimal)])
#                  index = first_elements.index(minimal)
 #           first_elements[index] = next(iter_array[first_elements.index(minimal)])
            """
        except StopIteration:
            index = first_elements.index(minimal)
            del first_elements[index]
            del iter_array[index]
            # if there are no more iterators
            if first_elements == []:
                break

if __name__ == '__main__':
    mass = [[1, 8, 16, 19], [3, 6, 7, 7, 7], [4, 11, 15, 44]]
    for n in do_sort(mass):
        print(n)
