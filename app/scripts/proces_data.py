def merge_dict(json0, json1):
    res = {}
    for each in json0.keys():
        if (len(json1.keys()) < 1):
            res.update({each: json0[each]})
        for key in json1.keys():
            if each == key:
                res.update({key: merge_dict(json0[key], json1[key])})
            else:
                res.update({each: json0[each]})
    print(res)
    return res


def merge_dict2(res, data):
    response = {}
    if (len(data.keys()) < 1):
        return res
    for each in res.keys():
        for key in data.keys():
            if each == key:
                response.update({key: merge_dict(res[key], data[key])})
            else:
                response.update({each: res[each]})
    return response
