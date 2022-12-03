from app import getRandomAdvice, getRandomPoem, getRandomJoke
def test_getRandomAdvice():
    advice = getRandomAdvice()
    assert advice != None

def test_getRandomPoem():
    advice = getRandomPoem()
    assert advice != None

def test_getRandomJoke():
    advice = getRandomJoke()
    assert advice != None
