# Reference: https://github.com/ztane/python-Levenshtein/issues/34#issuecomment-626118434


import Levenshtein


def levenshtein_editops_list(source, target):
    unique_elements = sorted(set(source + target))
    char_list = [chr(i) for i in range(len(unique_elements))]
    if len(unique_elements) > len(char_list):
        raise Exception("too many elements")
    else:
        unique_element_map = {ele:char_list[i]  for i, ele in enumerate(unique_elements)}
    source_str = ''.join([unique_element_map[ele] for ele in source])
    target_str = ''.join([unique_element_map[ele] for ele in target])
    transform_list = Levenshtein.editops(source_str, target_str)
    return transform_list

def levenshtein_list(source, target):
    editops = levenshtein_editops_list(source, target)
    return len(editops)
