def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        for key in kwargs:
            kwargs[key] = str[kwargs(key)]
        
        return func(*args, **kwargs)
    
    return decorator_wrapper


@only_strings
def convert_to_str(**kwargs):
    return ', '.join(**kwargs.values())


lst = ['one', 'two', 'three', 'four', 'five', 3]
joined_str = convert_to_str(kw1=1, kw2='two', kw3=3, kw4='four')

print(joined_str)
print(type(joined_str))