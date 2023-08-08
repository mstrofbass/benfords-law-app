def test_request_example(client):
    response = client.get("/")
    assert b'data-id="main-content"' in response.data
