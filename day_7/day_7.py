import sys


def parse_input(sample=True, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    lines = open(filename).read().splitlines()
    path = []
    tree = {}
    for line in lines:
        if line.startswith('$'):
            command = line[2:].split(' ')
            if len(command) == 2:
                if command[-1] == '..':
                    path.pop()
                else:
                    path.append(command[-1])
                continue
            else:
                continue
        key = ''.join(path)
        if key not in tree:
            tree[key] = []
        parts = line.split(' ')
        if parts[0] == 'dir':
            tree[key].append((parts[1], '-'))
        else:
            size, name = parts
            tree[key].append((name, size))
    if verbose:
        print(tree)
    return tree


# def tree_to_json(current, parts, path, tree, verbose=False):
#     result = {}
#     if verbose:
#         print(current, parts, path)
#     if current not in result:
#         result[current] = {}
#     for part in parts:
#         name, value = part
#         if value != '-':
#             result[current].update({name: value})
#         else:
#             new_current = name
#             new_parts = tree[''.join(path) + current + name]
#             new_path = path + [current]
#             result[current].update(tree_to_json(new_current, new_parts, new_path, tree))

#     return result

def tree_to_json(current, path, tree, verbose=False):
    result = {}
    full_path = ''.join(path) + current
    parts = tree[full_path]
    if verbose:
        print(current, parts, path)
    if current not in result:
        result[current] = {}
    for part in parts:
        name, value = part
        if value != '-':
            result[current].update({name: value})
        else:
            result[current].update(tree_to_json(name, path + [current], tree))

    return result


def pretty_print(tree, spacing=""):
    for key, value in tree.items():
        if isinstance(value, dict):
            print(spacing + key)
            pretty_print(tree[key], spacing + " ")
        else:
            print(f'{spacing}{key}: {value}')


def calc_size(path, tree):
    size = 0
    content = tree[path]
    for c in content:
        name, value = c
        if value == '-':
            size = size + calc_size(path + name, tree)
        else:
            size = size + int(value)
    return size


def part_1(tree):
    sizes = []
    for key, _ in tree.items():
        size = calc_size(key, tree)
        sizes.append((key, size))
    if verbose:
        print(sizes)

    wanted = map(lambda item: item[1], filter(lambda value: value[1] <= 100000, sizes))

    print(sum(wanted))

    return sizes


def part_2(sizes):
    total_disk_space = 70000000
    required_free_space = 30000000

    _, current_used_space = sizes[0]
    current_free_space = total_disk_space - current_used_space
    sorted_sizes = sorted(sizes, key=lambda x: x[1])
    for s in sorted_sizes:
        _, value = s
        if current_free_space + value >= required_free_space:
            print(value)
            break


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    tree = parse_input(sample=sample, verbose=verbose)
    if verbose:
        json_tree = tree_to_json(current='/', path=[], tree=tree)
        pretty_print(json_tree)
    sizes = part_1(tree)
    part_2(sizes)
    