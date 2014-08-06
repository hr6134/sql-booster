def tuple_to_dict(tpl):
    dct = {}
    n1 = 0
    for i in tpl:
        n2 = 1
        tmp = {}
        for j in i:
            tmp[str(n2)] = str(j)
            n2 += 1
        dct[n1] = tmp
        n1 += 1

    return dct


def tuple_to_dict_with_meta(tpl, meta):
    dct = {}
    n1 = 0
    for i in tpl:
        n2 = 0
        tmp = {}
        for j in i:
            tmp[meta[n2]] = str(j)
            n2 += 1
        dct[n1] = tmp
        n1 += 1

    return dct


def group_select_diff(group_tpl, select_tpl):
    tmp = []
    for i in select_tpl:
        if not i in group_tpl:
            tmp.append(i)

    return tmp
