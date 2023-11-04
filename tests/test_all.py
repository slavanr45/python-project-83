from page_analyzer.app import index, dotenv_path


def test_first():
    assert index() == 'Hello world!'
    assert dotenv_path
