# removes www and https:// from keys and values in a dictionary
def remove_www(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        if key.startswith("www."):
            new_key = key[4:]
        elif key.startswith("https://"):
            new_key = key[12:]
        else:
            new_key = key

        if value.startswith("www."):
            new_value = value[4:]
        elif value.startswith("https://"):
            new_value = value[12:]
        else:
            new_value = value

        new_dict[new_key] = new_value

    return new_dict


# removes www and https:// from keys in a dictionary
def remove_www_fKey(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        if key.startswith("www."):
            new_dict[key[4:]] = value
        elif key.startwith("https://"):
            new_dict[key[12:]] = value
        else:
            new_dict[key] = value
    return new_dict



# removes www and https:// from values in a dictionary
def remove_www_fVal(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        if value.startswith("www."):
            new_dict[key] = value[4:]
        elif value.startswith("https://"):
            new_dict[key] = value[12:]
        else:
            new_dict[key] = value
    return new_dict