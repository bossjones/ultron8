import pytest

from ultron8.utils.ip_utils import is_ipv4, is_ipv6, split_host_port


class TestIPUtilsTests:
    def test_host_port_split(self):

        # Simple IPv4
        host_str = "1.2.3.4"
        host, port = split_host_port(host_str)
        assert host == host_str
        assert port == None

        # Simple IPv4 with port
        host_str = "1.2.3.4:55"
        host, port = split_host_port(host_str)
        assert host == "1.2.3.4"
        assert port == 55

        # Simple IPv6
        host_str = "fec2::10"
        host, port = split_host_port(host_str)
        assert host == "fec2::10"
        assert port == None

        # IPv6 with square brackets no port
        host_str = "[fec2::10]"
        host, port = split_host_port(host_str)
        assert host == "fec2::10"
        assert port == None

        # IPv6 with square brackets with port
        host_str = "[fec2::10]:55"
        host, port = split_host_port(host_str)
        assert host == "fec2::10"
        assert port == 55

        # IPv4 inside bracket
        host_str = "[1.2.3.4]"
        host, port = split_host_port(host_str)
        assert host == "1.2.3.4"
        assert port == None

        # IPv4 inside bracket and port
        host_str = "[1.2.3.4]:55"
        host, port = split_host_port(host_str)
        assert host == "1.2.3.4"
        assert port == 55

        # Hostname inside bracket
        host_str = "[st2build001]:55"
        host, port = split_host_port(host_str)
        assert host == "st2build001"
        assert port == 55

        # Simple hostname
        host_str = "st2build001"
        host, port = split_host_port(host_str)
        assert host == "st2build001"
        assert port == None

        # Simple hostname with port
        host_str = "st2build001:55"
        host, port = split_host_port(host_str)
        assert host == "st2build001"
        assert port == 55

        # No-bracket invalid port
        host_str = "st2build001:abc"
        with pytest.raises(Exception):
            split_host_port(host_str)
        # self.assertRaises(Exception, split_host_port, host_str)

        # Bracket invalid port
        host_str = "[fec2::10]:abc"
        # self.assertRaises(Exception, split_host_port, host_str)
        with pytest.raises(Exception):
            split_host_port(host_str)

        # Validate ipv6 str
        host_str = "fd9a:49c7:f8dd:5156:0:0:0:0"
        res = is_ipv6(host_str)
        assert res

        # invalid ipv6 str
        host_str = "fd9a:49c7:f8dd:5156:0:0:0:0:0"
        res = is_ipv6(host_str)
        assert not res

        # Validate ipv4 str
        host_str = "127.0.0.1"
        res = is_ipv4(host_str)
        assert res

        # invalid ipv4 str
        host_str = "127.0.0.1.1"
        res = is_ipv4(host_str)
        assert not res
