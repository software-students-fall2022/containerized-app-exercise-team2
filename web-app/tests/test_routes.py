def test_login_page(app_with_data):
    url='/'
    response= app_with_data.get(url)
    assert response.status_code == 200

def test_login(app_with_data):
    url='/'
    response= app_with_data.get(url, query_string={'username': 'test', 'password':'test'},follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path=='/home'