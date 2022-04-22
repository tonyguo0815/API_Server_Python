import json;

def ResultPackage(result, keys):
    list = [];
    
    for item in result:
        if (len(item) != len(keys)):
            return 'Check Keys';
        package = {};
        count = 0;
        for key in keys:
            package[key] = item[count];
            count +=1;

        list.append(package);

    return json.dumps(list);