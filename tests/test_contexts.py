from pycontexts import __version__, push, pop, get, get_dict

def test_version():
    assert __version__ == '0.1.0'

def test_push_pop():
    push(a=1, b=2)
    assert get_dict('a', 'b') == dict(a=1, b=2)
    assert get('a') == 1
    assert get('b') == 2
    push(a=3, b=4)
    assert get_dict('a', 'b') == dict(a=3, b=4)
    assert pop('a') == 3
    assert get_dict('a', 'b') == dict(a=1, b=4)
    assert pop('b') == 4
    assert get_dict('a', 'b') == dict(a=1, b=2)
    assert pop('a') == 1
    assert get_dict('a', 'b') == dict(b=2)
    assert pop('b') == 2
    assert get_dict('a', 'b') == dict()
