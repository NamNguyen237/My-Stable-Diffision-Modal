string =list(input('enter generated tags: ').split(', '))
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result
print(" ")
print(", ".join(str(x) for x in remove_duplicates(string)))