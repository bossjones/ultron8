import pytest

from ultron8.api.utils.parser import get_domain_from_fqdn


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "http://stackoverflow.com:8080/some/folder?test=/questions/9626535/get-domain-name-from-url",
            "stackoverflow.com",
        ),
        (
            "Stackoverflow.com:8080/some/folder?test=/questions/9626535/get-domain-name-from-url",
            "stackoverflow.com",
        ),
        (
            "http://stackoverflow.com/some/folder?test=/questions/9626535/get-domain-name-from-url",
            "stackoverflow.com",
        ),
        (
            "https://StackOverflow.com:8080?test=/questions/9626535/get-domain-name-from-url",
            "stackoverflow.com",
        ),
        (
            "stackoverflow.com?test=questions&v=get-domain-name-from-url",
            "stackoverflow.com",
        ),
    ],
)
def test_get_domain_from_fqdn(test_input: str, expected: str) -> None:
    assert str(get_domain_from_fqdn(test_input)) == expected
