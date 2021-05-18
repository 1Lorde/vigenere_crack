def read_file(filename):
    with open(filename, 'r', encoding="utf8") as f:
        return f.read()


def write_file(filename, text):
    with open(filename, 'w', encoding="utf8") as f:
        f.writelines(text)


def print_dict(d):
    print("\n".join("{!r}: {!r}".format(k, v) for k, v in d.items()))


def sort_dictionary_by_key(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[0]))


def sort_dictionary_by_value(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
