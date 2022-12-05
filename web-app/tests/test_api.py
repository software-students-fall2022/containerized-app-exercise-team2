from app import getRandomAdvice, getRandomPoem, getRandomJoke
def test_getRandomAdvice():
    advice = getRandomAdvice()
    assert isinstance(advice, str)
    assert advice != None

def test_getRandomPoem():
    poem = getRandomPoem()
    assert isinstance(poem, str)
    assert poem != None

def test_getRandomJoke():
    joke = getRandomJoke()
    assert isinstance(joke, str)
    assert joke != None


def test_type_getRandomAdvice():
    advice = getRandomAdvice()
    assert isinstance(advice, str)

def test_type_getRandomPoem():
    poem = getRandomPoem()
    assert isinstance(poem, str)

def test_type_getRandomJoke():
    joke = getRandomJoke()
    assert isinstance(joke, str)
