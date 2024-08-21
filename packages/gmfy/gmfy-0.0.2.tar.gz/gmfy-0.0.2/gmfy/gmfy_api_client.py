from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from gmfy.exceptions import GMFYClientError
from gmfy.gmfy_endpoints import GMFYEndpoints
from gmfy.utils import get_http_modules

httpx, requests = get_http_modules()

if TYPE_CHECKING:
    from gmfy.base_payment import BasePayment
    from gmfy.event_manager import EventManager, SingleEventManager

logger = logging.getLogger(__name__)


class GMFYApiClientBase:
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        self.headers = {
            "x-api-key": self.token,
            "Content-Type": "application/json",
        }


class GMFYApiClientSync(GMFYApiClientBase):
    def __init__(self, token: str, url: str):
        super().__init__(token, url)
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _get(self, url: str, **kwargs) -> requests.Response:  # type: ignore[name-defined]
        try:
            params = kwargs.get("params", {})
            response = self.session.get(url, timeout=60, verify=False, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise GMFYClientError(f"Bad response status for {url}") from error
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.RequestException,
        ) as error:
            raise GMFYClientError("Network error when fetching gmfy") from error
        else:
            logging.info("Successful GET request to %s", url)
            return response

    def _post(self, url: str, data: Any) -> requests.Response:  # type: ignore[name-defined]
        try:
            response = self.session.post(
                url=url,
                data=data,
                timeout=60,
                verify=False,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise GMFYClientError(f"Bad response status for {url}") from error
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.RequestException,
        ) as error:
            raise GMFYClientError("Network error when fetching gmfy") from error
        else:
            logging.info("Successful POST request to %s", url)
            return response

    def create_events(self, event_manager: EventManager) -> requests.Response:  # type: ignore[name-defined]
        dumped_events = event_manager.model_dump_json(by_alias=True)
        return self._post(GMFYEndpoints.events_batch, dumped_events)

    def create_event(self, event_manager: SingleEventManager) -> requests.Response:  # type: ignore[name-defined]
        dumped_event = event_manager.model_dump_json(by_alias=True)
        return self._post(GMFYEndpoints.events, dumped_event)

    def create_payment(self, payment: BasePayment) -> requests.Response:  # type: ignore[name-defined]
        dumped_payment = payment.model_dump_json(by_alias=True)
        return self._post(GMFYEndpoints.payments, dumped_payment)

    def create_resend_code(self, payment_id: str) -> requests.Response:  # type: ignore[name-defined]
        return self._post(f"{GMFYEndpoints.payments}{payment_id}/resend-code", None)

    def get_version(self) -> requests.Response:  # type: ignore[name-defined]
        return self._get(GMFYEndpoints.version)

    def get_users(self, user_id: str | None) -> requests.Response:  # type: ignore[name-defined]
        if user_id:
            return self._get(f"{GMFYEndpoints.users}{user_id}")
        return self._get(GMFYEndpoints.users)

    def get_rating_top_users(
        self,
        rating_id: str,
        params: dict[str, Any],
    ) -> requests.Response:  # type: ignore[name-defined]
        return self._get(f"{GMFYEndpoints.ratings}{rating_id}/top", params=params)

    def get_challenge_top_users(
        self,
        challenge_id: str,
        params: dict[str, Any],
    ) -> requests.Response:  # type: ignore[name-defined]
        return self._get(f"{GMFYEndpoints.challenges}{challenge_id}/top", params=params)

    def get_user_badges(self, user_id: str) -> requests.Response:  # type: ignore[name-defined]
        return self._get(f"{GMFYEndpoints.badges}{user_id}")

    def get_notifications(self, user_id: str) -> requests.Response:  # type: ignore[name-defined]
        return self._get(f"{GMFYEndpoints.notifications}{user_id}")

    def get_payment(self, payment_id: str) -> requests.Response:  # type: ignore[name-defined]
        return self._get(f"{GMFYEndpoints.payments}{payment_id}")

    def close(self) -> None:
        self.session.close()


class GMFYApiClientAsync(GMFYApiClientBase):
    def __init__(self, token: str, url: str):
        super().__init__(token, url)
        self.session = httpx.AsyncClient(
            headers=self.headers,
            verify=False,
        )

    async def _get(self, url: str, **kwargs: Any) -> httpx.Response:  # type: ignore[name-defined]
        try:
            params = kwargs.get("params", {})
            response = await self.session.get(url, timeout=60, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise GMFYClientError(f"Bad response status for {url}") from error
        except (
            httpx.ConnectError,
            httpx.TimeoutException,
            httpx.RequestError,
        ) as error:
            raise GMFYClientError("Network error when fetching gmfy") from error
        else:
            logging.info("Successful GET request to %s", url)
            return response

    async def _post(self, url: str, data: Any) -> httpx.Response:  # type: ignore[name-defined]
        try:
            response = await self.session.post(
                url=url,
                data=data,
                timeout=60,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise GMFYClientError(f"Bad response status for {url}") from error
        except (
            httpx.ConnectError,
            httpx.TimeoutException,
            httpx.RequestError,
        ) as error:
            raise GMFYClientError("Network error when fetching gmfy") from error
        else:
            logging.info("Successful POST request to %s", url)
            return response

    async def create_events(self, event_manager: EventManager) -> httpx.Response:  # type: ignore[name-defined]
        dumped_events = event_manager.model_dump_json(by_alias=True)
        return await self._post(GMFYEndpoints.events_batch, dumped_events)

    async def create_event(self, event_manager: EventManager) -> httpx.Response:  # type: ignore[name-defined]
        dumped_event = event_manager.model_dump_json(by_alias=True)
        return await self._post(GMFYEndpoints.events, dumped_event)

    async def create_payment(self, payment: BasePayment) -> httpx.Response:  # type: ignore[name-defined]
        dumped_payment = payment.model_dump_json(by_alias=True)
        return await self._post(GMFYEndpoints.payments, dumped_payment)

    async def create_resend_code(self, payment_id: str) -> httpx.Response:  # type: ignore[name-defined]
        return await self._post(
            f"{GMFYEndpoints.payments}{payment_id}/resend-code",
            None,
        )

    async def get_version(self) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(GMFYEndpoints.version)

    async def get_users(self, user_id: str | None) -> httpx.Response:  # type: ignore[name-defined]
        if user_id:
            return await self._get(f"{GMFYEndpoints.users}{user_id}")
        return await self._get(GMFYEndpoints.users)

    async def get_rating_top_users(
        self,
        rating_id: str,
        params: dict[str, Any],
    ) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(f"{GMFYEndpoints.ratings}{rating_id}/top", params=params)

    async def get_challenge_top_users(
        self,
        challenge_id: str,
        params: dict[str, Any],
    ) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(
            f"{GMFYEndpoints.challenges}{challenge_id}/top",
            params=params,
        )

    async def get_user_badges(self, user_id: str) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(f"{GMFYEndpoints.badges}{user_id}")

    async def get_notifications(self, user_id: str) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(f"{GMFYEndpoints.notifications}{user_id}")

    async def get_payment(self, payment_id: str) -> httpx.Response:  # type: ignore[name-defined]
        return await self._get(f"{GMFYEndpoints.payments}{payment_id}")

    async def close(self) -> None:
        await self.session.aclose()
