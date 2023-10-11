def merge_dict(json0, json1):
    res = json0
    for each in json0.keys():
        for key in json1.keys():
            if each == key:
                res.update({key: merge_dict(json0[key], json1[key])})
            else:
                res.update(json0)
                res.update(json1)
    return res
