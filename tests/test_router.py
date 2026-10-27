import pytest
import responses
from requests.exceptions import ConnectionError
from unittest.mock import MagicMock, patch

from tenda_4g09 import Tenda4G09


@pytest.fixture
def router() -> Tenda4G09:
    """Create a router instance with mocked authentication."""
    client = Tenda4G09("192.168.0.1", "admin123")
    client.auth = MagicMock()
    return client


def test_context_manager(router: Tenda4G09) -> None:
    """Verify that the context manager logs in and logs out correctly."""
    with router as client:
        assert client is router
        router.auth.login.assert_called_once_with()

    router.auth.logout.assert_called_once_with()


@responses.activate
def test_request_success(router: Tenda4G09) -> None:
    """Verify that _request returns and parses a successful JSON response."""
    responses.add(
        responses.GET,
        "http://192.168.0.1/goform/testEndpoint",
        json={"status": "ok", "value": 42},
        status=200,
    )

    data = router._request("GET", "/goform/testEndpoint")

    assert data["value"] == 42
    assert data["status"] == "ok"


@responses.activate
def test_request_raises_login_required(router: Tenda4G09) -> None:
    """Verify that an HTML login page triggers a login-required error."""
    html_response = (
        '<html><head><meta name="description" content="login">'
        "</head><body></body></html>"
    )

    responses.add(
        responses.GET,
        "http://192.168.0.1/goform/protectedEndpoint",
        body=html_response,
        status=200,
    )

    with pytest.raises(RuntimeError, match="Login required"):
        router._request("GET", "/goform/protectedEndpoint")

    router.auth.logged_out.assert_called_once_with()


@responses.activate
@patch("tenda_4g09.models.RouterStatus.from_dict")
def test_get_status(
    mock_from_dict: MagicMock,
    router: Tenda4G09,
) -> None:
    """Verify that router status is parsed and the host IP is updated."""
    mock_status = MagicMock()
    mock_status.lan_ip = "192.168.0.2"
    mock_from_dict.return_value = mock_status

    responses.add(
        responses.GET,
        "http://192.168.0.1/goform/GetRouterStatus",
        json={"fake_data": "yes"},
        status=200,
    )

    result = router.get_status()

    assert result == mock_status
    assert router._host_ip == "192.168.0.2"
    mock_from_dict.assert_called_once_with({"fake_data": "yes"})


@responses.activate
def test_enable_telnet_success(router: Tenda4G09) -> None:
    """Verify that Telnet is enabled successfully."""
    responses.add(
        responses.GET,
        "http://192.168.0.1/goform/telnet",
        body="load telnetd success.",
        status=200,
    )

    assert router.enable_telnet() is True


@responses.activate
def test_enable_telnet_connection_error(router: Tenda4G09) -> None:
    """Verify that a network connection error is handled correctly."""
    responses.add(
        responses.GET,
        "http://192.168.0.1/goform/telnet",
        body=ConnectionError("Network unreachable"),
    )

    assert router.enable_telnet() is False


@responses.activate
def test_system_reboot(router: Tenda4G09) -> None:
    """Verify that the reboot request uses POST with the expected payload."""
    responses.add(
        responses.POST,
        "http://192.168.0.1/goform/SysToolReboot",
        body="ok",
        status=200,
    )

    router.system_reboot()

    assert len(responses.calls) == 1

    request = responses.calls[0].request
    assert request.method == "POST"
    assert request.body == "action=0"
