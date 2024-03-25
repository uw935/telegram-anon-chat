import requests

from loguru import logger
from models import FactsResponse
from config import INTERESTING_FACTS_API


class Fact:
    @staticmethod
    async def get() -> FactsResponse:
        """
        Get random intersting fact from the API

        :return: FactsResponse from models
        """

        _request = requests.get(INTERESTING_FACTS_API)

        if _request.status_code != 200:
            logger.warning(
                "Error while getting interesting fact: "
                f"{_request.status_code} && {_request.json()}"
            )

            return FactsResponse(status=False)

        return FactsResponse(status=True, text=_request.json()["text"])
