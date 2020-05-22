from django_stripe.utils.request import get_client_ip


class TestGetClientIp:
    def test_with_default(self, rf):
        request = rf.get("/")
        ip = get_client_ip(request)
        assert ip == "127.0.0.1"

    def test_with_just_remote_addr(self, rf):
        request = rf.get("/", REMOTE_ADDR="127.0.0.1")
        ip = get_client_ip(request)
        assert ip == "127.0.0.1"

    def test_with_single_x_forwarded_for(self, rf):
        request = rf.get("/", REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="8.8.8.8")
        ip = get_client_ip(request)
        assert ip == "8.8.8.8"

    def test_with_multiple_x_forwarded_for(self, rf):
        request = rf.get(
            "/", REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="8.8.8.8,4.4.4.4"
        )
        ip = get_client_ip(request)
        assert ip == "4.4.4.4"
