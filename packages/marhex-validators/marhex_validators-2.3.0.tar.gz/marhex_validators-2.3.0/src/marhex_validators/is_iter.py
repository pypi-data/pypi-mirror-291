def is_persian_char(iterable):
    char_list = ' ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    result: bool
    try:
        for item in iterable:
            if item in char_list:
                result = True
            else:
                result = False
                break

        return result
    except:
        raise ValueError('[ iterable ] arg must be a Iterable Type')
