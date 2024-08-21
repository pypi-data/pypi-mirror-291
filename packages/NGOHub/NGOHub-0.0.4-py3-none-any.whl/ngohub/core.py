from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ngohub.network import HTTPClient, HTTPClientResponse


class BaseHub(ABC):
    """
    Abstract class used to define all the required methods for a hub interface
    """

    @abstractmethod
    def __init__(self, api_base_url: str) -> None:
        pass


class NGOHub(BaseHub):
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url: str = api_base_url or ""
        self.client: HTTPClient = HTTPClient(self.api_base_url)

    def is_healthy(self) -> bool:
        response: HTTPClientResponse = self.client.api_get("/health/")

        response_is_ok: bool = response.to_str() == "OK"

        return response_is_ok

    def get_version(self) -> Dict[str, str]:
        response: HTTPClientResponse = self.client.api_get("/version/")

        response_dict: Dict = response.to_dict()
        version_revision: Dict[str, str] = {
            "version": response_dict["version"],
            "revision": response_dict["revision"],
        }

        return version_revision

    def get_file_url(self, path: str) -> str:
        response: HTTPClientResponse = self.client.api_get(f"/file?path={path}")

        return response.to_str()

    def _get_nomenclature(self, nomenclature: str) -> Any:
        response: HTTPClientResponse = self.client.api_get(f"/nomenclatures/{nomenclature}")

        return response.to_dict()

    def get_cities_nomenclatures(
        self, search: str = None, county_id: int = None, city_id: int = None
    ) -> List[Dict[str, Any]]:
        mandatory_params: List[Any] = [search, county_id]
        if all(param is None for param in mandatory_params):
            raise ValueError("Please provide at least one of the following: county_id, search")

        search_query: List[str] = []
        if search:
            search_query.append(f"search={search}")
        if county_id:
            search_query.append(f"countyId={county_id}")
        if city_id:
            search_query.append(f"cityId={city_id}")

        return self._get_nomenclature(f"cities?{'&'.join(search_query)}")

    def get_counties_nomenclatures(self) -> List[Dict[str, Any]]:
        return self._get_nomenclature("counties")

    def get_domains_nomenclatures(self):
        return self._get_nomenclature("domains")

    def get_regions_nomenclatures(self):
        return self._get_nomenclature("regions")

    def get_federations_nomenclatures(self):
        return self._get_nomenclature("federations")

    def get_coalitions_nomenclatures(self):
        return self._get_nomenclature("coalitions")

    def get_faculties_nomenclatures(self):
        return self._get_nomenclature("faculties")

    def get_skills_nomenclatures(self):
        return self._get_nomenclature("skills")

    def get_practice_domains_nomenclatures(self):
        return self._get_nomenclature("practice-domains")

    def get_service_domains_nomenclatures(self):
        return self._get_nomenclature("service-domains")

    def get_beneficiaries_nomenclatures(self):
        return self._get_nomenclature("beneficiaries")

    def get_issuers_nomenclatures(self):
        return self._get_nomenclature("issuers")
