from page_analyzer.app import index


def test_first():
    assert index() == 'Hello world!'
