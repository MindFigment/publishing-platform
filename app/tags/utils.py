import re
from django.utils.functional import wraps


def parse_tags(tagstring):
    if not tagstring:
        return []

    tagregex = r'"([\w,\s]+)"|(\w+)'
    tags = [_get_matched(match) for match in re.findall(tagregex, tagstring)]
    tags.sort()
    return tags


# re.findall in our case returns a tuple of two groups for each match
# where one of the groups is always empty ('')
# so here we extract non-empty one
def _get_matched(tup):
    return tup[0] if len(tup[0]) else tup[1]


def format_tags_into_string(tags):
    names = []
    for tag in tags:
        name = tag.name
        if ',' in name or ' ' in name:
            names.append('"{}"'.format(name))
        else:
            names.append(name)
    return ', '.join(sorted(names))


def require_instance_manager(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError(
                f"Cant't call {func.__name__} with a non-instance manager"
            )
        return func(self, *args, **kwargs)
    return wrapper


if __name__ == '__main__':
    test1 = 'apple ball cat'
    test2 = 'apple, ball, cat'
    test3 = 'apple, ball cat'
    test4 = '"apple, ball" cat dog'
    test5 = '"apple, ball", cat dog'
    test6 = 'apple "ball cat" dog'
    test7 = '"apple" "ball dog'

    tests = (test1, test2, test3, test4, test5, test6, test7)

    print(50 * '-')
    print('TESTS START')
    print(50 * '-')
    for test in tests:
        words = parse_tags(test)
        print('{} -> {}'.format(test, words))
    print(50 * '-')
    print('TESTS END')
    print(50 * '-')
