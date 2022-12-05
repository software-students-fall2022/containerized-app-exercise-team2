import pytest
import app

def test_main_page():

    flask_app = app.app

    with flask_app.test_client() as test_client:
        response =test_client.get('/')
        print("success")
        assert response.status_code==200