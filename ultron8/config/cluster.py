"""Config, yaml based config object using the ruamel python module"""
# pylint: disable=line-too-long
# pylint: disable=W1202

from dataclasses import dataclass, field
import logging
import uuid

from ultron8.api.utils.parser import get_domain_from_fqdn

log = logging.getLogger(__name__)


@dataclass
class ClusterConfig:
    ultron_cluster_url: str
    ultron_acs_token: str
    ultron_uuid: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.ultron_uuid = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS, get_domain_from_fqdn(self.ultron_cluster_url)
            )
        )

    def __str__(self) -> str:
        return f"{self.ultron_cluster_url}{self.ultron_acs_token}"

    @classmethod
    def from_dict(cls, config):
        """Factory method for creating Settings object from env vars."""

        kwargs = dict(
            ultron_cluster_url=config.ultron_cluster_url,
            ultron_acs_token=config.ultron_acs_token,
        )

        return cls(**kwargs)


if __name__ == "__main__":
    data = {
        "ultron_cluster_url": "http://localhost:11267",
        "ultron_acs_token": "fdgjhregioerhjgoeirhjeroihjriodjhdifojbriohjeriohjerohijeroierhjeori",
    }
    c = ClusterConfig(**data)
