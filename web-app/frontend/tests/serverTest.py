import pytest
import app

@pytest.fixture
def app():
    app = create_app()
    return app