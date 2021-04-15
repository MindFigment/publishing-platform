from django.test import TestCase

from common.utils import add_markdown_to_links


class AddMarkdownToLinks(TestCase):
    def test_html_1(self):
        test_html = '''
            Changed my name back to Hall, sorry for the confusion.
            https://github.com/PacktPublishing/Django-3-by-Example/blob/master/Chapter06/bookmarks/images/templates/images/image/list_ajax.html
            Also, if you are interested, my video channel:
            https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ. See you!
        '''

        expected_output = '''
            Changed my name back to Hall, sorry for the confusion.
            <a href="https://github.com/PacktPublishing/Django-3-by-Example/blob/master/Chapter06/bookmarks/images/templates/images/image/list_ajax.html">https://github.com/PacktPublishing/Django-3-by-Example/blob/master/Chapter06/bookmarks/images/templates/images/image/list_ajax.html</a>
            Also, if you are interested, my video channel:
            <a href="https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ">https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ</a>. See you!
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)

    def test_html_2(self):
        test_html = '''
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            http://youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
        '''

        expected_output = '''
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            <a href="http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ">http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ</a>
            <a href="http://youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ">http://youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ</a>
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)

    def test_html_3(self):
        test_html = '''
            Changed my name back to Hall, sorry for the confusion.
            https://realpython.com/regex-python/#modified-regular-expression-matching-with-flags
            Also, if you are interested, my video channel:
            https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''
        expected_output = '''
            Changed my name back to Hall, sorry for the confusion.
            <a href="https://realpython.com/regex-python/#modified-regular-expression-matching-with-flags">https://realpython.com/regex-python/#modified-regular-expression-matching-with-flags</a>
            Also, if you are interested, my video channel:
            <a href="https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ">https://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ</a>
            Hmm...
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)

    def test_html_4(self):
        test_html = '''
            https://docs.python.org/3/library/re.html
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''
        expected_output = '''
            <a href="https://docs.python.org/3/library/re.html">https://docs.python.org/3/library/re.html</a>
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)

    def test_html_5(self):
        test_html = '''
            Changed my name back to Hall, sorry for the confusion.
            https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL.
            Also, if you are interested, my video channel:
            http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''
        expected_output = '''
            Changed my name back to Hall, sorry for the confusion.
            <a href="https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL">https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL</a>.
            Also, if you are interested, my video channel:
            <a href="http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ">http://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ</a>
            youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)

    def test_html_6(self):
        test_html = '''
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            htp://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''
        expected_output = '''
            Changed my name back to Hall, sorry for the confusion.
            Also, if you are interested, my video channel:
            htp://www.youtube.com/channel/UCMzT-mdCqoyEv_-YZVtE7MQ
            Hmm...
        '''

        result = add_markdown_to_links(test_html)
        self.assertEqual(result, expected_output)
