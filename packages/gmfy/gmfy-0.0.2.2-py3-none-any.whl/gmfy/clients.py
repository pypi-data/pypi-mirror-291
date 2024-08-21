from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from gmfy.event_manager import EventManager, SingleEventManager
from gmfy.exceptions import GMFYClientError
from gmfy.gmfy_api_client import GMFYApiClientAsync, GMFYApiClientSync, httpx, requests

if TYPE_CHECKING:
    from gmfy.base_payment import BasePayment

logger = logging.getLogger(__name__)


class GMFYClientSync:
    def __init__(self, api_key: str, base_url: str):
        self.api_sync_client = GMFYApiClientSync(api_key, base_url)

    def create_batch_events(self, events: list[dict[str, Any]]) -> requests.Response:
        try:
            logging.info("Creating batch events: %s", events)
            event_manager = EventManager(events)
            response = self.api_sync_client.create_events(event_manager)
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating events") from error
        else:
            logger.info(
                "Batch events created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    def create_event(self, event: dict[str, Any]) -> requests.Response:
        try:
            logging.info("Creating event: %s", event)
            event_manager = SingleEventManager(event)
            response = self.api_sync_client.create_event(event_manager)
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating event") from error
        else:
            logger.info(
                "Event created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    def create_payment(self, payment: BasePayment) -> requests.Response:
        try:
            logging.info("Creating payment: %s", payment)
            response = self.api_sync_client.create_payment(payment)
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating payment") from error
        else:
            logger.info(
                "Payment created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    def create_resend_code(self, payment_id: str) -> requests.Response:
        logger.info("Creating resend code for payment with id %s", payment_id)
        return self.api_sync_client.create_resend_code(payment_id)

    def get_api_version(self) -> requests.Response:
        logger.info("Getting API version")
        return self.api_sync_client.get_version()

    def get_users(self, user_id: str | None = None) -> requests.Response:
        logger.info("Getting users")
        return self.api_sync_client.get_users(user_id)

    def get_rating_top_users(
        self,
        rating_id: str,
        offset: int = 0,
        limit: int = 10,
        sort: str = "ASC",
    ) -> requests.Response:
        logger.info("Getting top users in rating with id %s", rating_id)
        params = {"offset": offset, "limit": limit, "sort": sort}
        return self.api_sync_client.get_rating_top_users(rating_id, params=params)

    def get_challenge_top_users(
        self,
        challenge_id: str,
        limit: int = 10,
    ) -> requests.Response:
        logger.info("Getting top users in challenge with id %s", challenge_id)
        params = {"limit": limit}
        return self.api_sync_client.get_challenge_top_users(challenge_id, params=params)

    def get_user_badges(self, user_id: str) -> requests.Response:
        logger.info("Getting badges for user with id %s", user_id)
        return self.api_sync_client.get_user_badges(user_id)

    def get_notifications(self, user_id: str) -> requests.Response:
        logger.info("Getting notifications for user with id %s", user_id)
        return self.api_sync_client.get_notifications(user_id)

    def get_payment(self, payment_id: str) -> requests.Response:
        logger.info("Getting payment with id %s", payment_id)
        return self.api_sync_client.get_payment(payment_id)


class GMFYClientAsync:
    def __init__(self, api_key: str, base_url: str):
        self.api_async_client = GMFYApiClientAsync(api_key, base_url)

    async def create_batch_events(self, events: list[dict[str, Any]]) -> httpx.Response:
        try:
            logging.info("Creating batch events: %s", events)
            event_manager = EventManager(events)
            response = await self.api_async_client.create_events(
                event_manager,
            )
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating events") from error
        else:
            logger.info(
                "Batch events created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    async def create_event(self, event: dict[str, Any]) -> requests.Response:
        try:
            logging.info("Creating event: %s", event)
            event_manager = EventManager([event])
            response = await self.api_async_client.create_event(event_manager)
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating event") from error
        else:
            logger.info(
                "Event created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    async def create_payment(self, payment: BasePayment) -> requests.Response:
        try:
            logging.info("Creating payment: %s", payment)
            response = await self.api_async_client.create_payment(payment)
        except ValidationError as error:
            raise GMFYClientError("Validation error while creating payment") from error
        else:
            logger.info(
                "Payment created successfully. Status code: %s. Response: %s",
                response.status_code,
                response.text,
            )
            return response

    async def create_resend_code(self, payment_id: str) -> httpx.Response:
        logger.info("Creating resend code for payment with id %s", payment_id)
        return await self.api_async_client.create_resend_code(payment_id)

    async def get_api_version(self) -> httpx.Response:
        logger.info("Getting API version")
        return await self.api_async_client.get_version()

    async def get_users(self, user_id: str | None = None) -> requests.Response:
        logger.info("Getting users")
        return await self.api_async_client.get_users(user_id)

    async def get_rating_top_users(
        self,
        rating_id: str,
        offset: int = 0,
        limit: int = 10,
        sort: str = "ASC",
    ) -> requests.Response:
        logger.info("Getting top users in rating with id %s", rating_id)
        params = {"offset": offset, "limit": limit, "sort": sort}
        return await self.api_async_client.get_rating_top_users(
            rating_id,
            params=params,
        )

    async def get_challenge_top_users(
        self,
        challenge_id: str,
        limit: int = 10,
    ) -> requests.Response:
        logger.info("Getting top users in challenge with id %s", challenge_id)
        params = {"limit": limit}
        return await self.api_async_client.get_challenge_top_users(
            challenge_id,
            params=params,
        )

    async def get_user_badges(self, user_id: str) -> requests.Response:
        logger.info("Getting badges for user with id %s", user_id)
        return await self.api_async_client.get_user_badges(user_id)

    async def get_notifications(self, user_id: str) -> requests.Response:
        logger.info("Getting notifications for user with id %s", user_id)
        return await self.api_async_client.get_notifications(user_id)

    async def get_payment(self, payment_id: str) -> requests.Response:
        logger.info("Getting payment with id %s", payment_id)
        return await self.api_async_client.get_payment(payment_id)
