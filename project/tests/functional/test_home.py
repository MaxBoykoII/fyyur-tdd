def test_home(test_app):
    client = test_app.test_client()
    resp = client.get('/')
    assert '200' in resp.status
    assert 'text/html' in resp.content_type