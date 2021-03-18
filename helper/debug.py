def dump_object(obj):
    print(type(obj))

    for key in obj.__dict__:
        print(f'{key} = {getattr(obj, key)}')