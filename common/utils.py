from django.core.checks.messages import Error
from django.template.defaultfilters import slugify

import re


def unique_slugify(instance, values, queryset=None, slug_field_name='slug', slug_seperator='-', max_num=1000):
    slug_field = instance._meta.get_field(slug_field_name)
    max_len = slug_field.max_length
    slug = slugify(values)
    if max_len:
        slug = slug[:max_len]

    if queryset is None:
        queryset = instance.__class__._default_manager.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    original_slug = slug

    num = 1
    while len(queryset.filter(**{slug_field_name: slug})) != 0:
        slug = original_slug
        end = f'{slug_seperator}{num}'
        if len(slug) + len(end) > max_len:
            overflow = len(slug) + len(end) - max_len
            slug = slug[:-overflow]

        slug = ''.join([slug, end])

        num += 1
        if num > max_num:
            raise Error(f'Over {max_num} slugs with the same base!')

    # setattr(instance, slug_field_name, slug)

    return slug


test_html_1 = '''
    Changed my name back to Hall, sorry for the confusion.
    https://github.com/PacktPublishing/Django-3-by-Example/blob/master/Chapter06/bookmarks/images/templates/images/image/list_ajax.html
    Also, if you are interested, my video channel:
    https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ. See you!
'''

test_html_2 = '''
    Changed my name back to Hall, sorry for the confusion.
    Also, if you are interested, my video channel:
    http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    http://youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
'''

test_html_3 = '''
    Changed my name back to Hall, sorry for the confusion.
    https://realpython.com/regex-python/#modified-regular-expression-matching-with-flags
    Also, if you are interested, my video channel:
    https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    Hmm...
'''

test_html_4 = '''
    https://docs.python.org/3/library/re.html
    Changed my name back to Hall, sorry for the confusion.
    Also, if you are interested, my video channel:
    www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    Hmm...
'''

test_html_5 = '''
    Changed my name back to Hall, sorry for the confusion.
    https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL.
    Also, if you are interested, my video channel:
    http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    Hmm...
'''

test_html_6 = '''
    Changed my name back to Hall, sorry for the confusion.
    Also, if you are interested, my video channel:
    htp://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
    Hmm...
'''

tests_html = (test_html_1,
              test_html_2,
              test_html_3,
              test_html_4,
              test_html_5,
              test_html_6)


def add_markdown_to_links(text=None):
    regex = r'''(
                # scheme:// (https://)
                (?:(?:http|https)://){1}
                # domain name (no port so not authority) (www.example.com)
                (?:www\.)?(?:[a-z]+\.)*(?:[a-z]+)
                # path (/path/to/myfile.html)
                (?:/[a-zA-Z0-9_-]*)*(?:\.html)?
                # query/parameters (?key1=value1&key2=value2)
                (?:\?[a-z0-9]=[a-z0-9](?:[&;][a-z0-9]=[a-z0-9])*)?
                # anchor (#SomewhereInTheDocument)
                (?:\#(?:[a-zA-Z0-9_-]*))?
                )
                '''

    # for i, test_html in enumerate(tests_html, 1):
    # print(i, '->', re.sub(regex, _add_a_tag, test_html, flags=re.VERBOSE))
    # match = re.finditer(regex, test_html, re.VERBOSE)
    # for url_match in match:
    #     print(url_match)
    #     print(re.sub())
    #     print(_add_a_tag(url_match[0]))
    return re.sub(regex, _add_a_tag, text, flags=re.VERBOSE)


def _add_a_tag(match_obj):
    HTML_LINK = '<a href="{0}">{0}</a>'
    url = match_obj.group(0)
    return HTML_LINK.format(url)


if __name__ == '__main__':
    add_markdown_to_links()
