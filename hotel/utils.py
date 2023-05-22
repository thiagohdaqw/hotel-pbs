def iter_all_items(dict_):
    for (type_, items) in dict_.items():
        yield from iter_list(type_, items)


def iter_list(type, list_):
    for index in range(len(list_)):
        yield f"{type}{index}"


def count_items(items):
    return sum(len(x) for x in items.values())
