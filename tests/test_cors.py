def test_cors_header_present_for_allowed_origin(api_client):
    resp = api_client.get("/api/health/", HTTP_ORIGIN="http://localhost:3000")
    assert resp.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"


def test_cors_header_absent_for_disallowed_origin(api_client):
    resp = api_client.get("/api/health/", HTTP_ORIGIN="http://evil.example.com")
    assert "Access-Control-Allow-Origin" not in resp.headers
