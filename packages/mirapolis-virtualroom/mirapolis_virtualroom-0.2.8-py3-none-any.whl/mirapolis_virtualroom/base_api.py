import logging
from hashlib import md5
from json import dumps
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from aiohttp import ClientConnectionError, ClientSession


class BaseAPI:
    def __init__(
        self,
        api_link: str,
        secret_key: str,
        app_id: str,
        verify_ssl: bool = False,
    ):
        self._link = api_link
        self._verify_ssl = verify_ssl

        self._secret_key = secret_key
        self._app_id = app_id

        self._api_link = api_link
        self._base_params = {
            "appid": self._app_id,
            "secretkey": self._secret_key,
        }

        self._headers = {
            "Accept": "*/*",
        }

    async def _prepare_params(self, route: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        url_parts = list(urlparse(self._api_link + route))
        query = dict(parse_qsl(url_parts[4]))

        params.update(self._base_params)
        query.update(params)

        url_parts[4] = urlencode(query)

        legacy_url = urlunparse(url_parts)
        md5_hash = md5(legacy_url.encode())
        sign = md5_hash.hexdigest().upper()

        encrypted_params = {"appid": self._app_id, "sign": sign}
        params.update(encrypted_params)
        params.pop("secretkey")
        return params

    async def _get(self, route: str, params: Optional[dict] = None):
        """
        Send get request to host
        :param params: request params
        :param route: request link
        :return: json object from host
        """
        params = await self._prepare_params(route, params)
        logging.info(f"GET {self._link}{route} {params=}")
        try:
            async with ClientSession(headers=self._headers) as session:
                async with session.get(
                    url=f"{self._link}{route}",
                    params=params,
                    verify_ssl=self._verify_ssl,
                ) as get:
                    if get.ok:
                        if get.content_type == "text/plain":
                            answer = await get.text()
                            logging.info(
                                f"GET {get.status} {
                                self._link}{route} {get.content_type} {answer=}"
                            )
                            return answer
                        answer = await get.json()
                        logging.info(
                            f"GET {get.status} {
                            self._link}{route} {get.content_type} {answer=}"
                        )
                        if "Content-Range" in get.headers:
                            logging.info(f"GET Content-Range: {get.headers["Content-Range"]}")
                            count = int(get.headers["Content-Range"].split("/")[-1])
                            return {"data": answer, "count": count}
                        else:
                            return answer
                    else:
                        logging.warning(
                            f"GET {get.status} {
                            self._link}{route}"
                        )
                        error = await get.json()
                        raise ClientConnectionError(error)
        except ClientConnectionError as e:
            logging.warning(f"Api error: {self._link}{route} {e}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def _post(
        self,
        route: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Optional[dict | str]:
        """
        Send post request to host
        :param params: request params
        :param data: request data
        :param route: request link
        :return: json object from host
        """
        params = await self._prepare_params(route, params)
        logging.info(f"POST {self._link}{route} {params=} {data=}")
        headers = {"Content-Type": "application/json"}
        try:
            async with ClientSession(headers=headers) as session:
                async with session.post(
                    f"{self._link}{route}",
                    params=params,
                    data=dumps(data, indent=4),
                    verify_ssl=self._verify_ssl,
                ) as post:
                    if post.ok:
                        if post.content_type == "text/plain":
                            answer = await post.text()
                            logging.info(
                                f"POST {post.status} {
                                self._link}{route} {post.content_type} {answer=}"
                            )
                            return answer
                        answer = await post.json()
                        logging.info(
                            f"POST {post.status} {
                            self._link}{route} {post.content_type} {answer=}"
                        )
                        return answer
                    else:
                        logging.warning(
                            f"POST {post.status} {
                            self._link}{route}"
                        )
                        error = await post.json()
                        raise ClientConnectionError(error)
        except ClientConnectionError as e:
            logging.warning(f"Api error: {self._link}{route} {e}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def _delete(self, route: str, params: Optional[dict] = None) -> Optional[int]:
        params = await self._prepare_params(route, params)
        logging.info(f"DELETE {self._link}{route} {params=}")
        try:
            async with ClientSession(headers=self._headers) as session:
                async with session.delete(
                    url=f"{self._link}{route}",
                    params=params,
                    verify_ssl=self._verify_ssl,
                ) as delete:
                    if delete.ok:
                        logging.info(
                            f"DELETE {delete.status} {
                            self._link}{route}"
                        )
                        return delete.status
                    else:
                        logging.warning(
                            f"DELETE {delete.status} {
                            self._link}{route}"
                        )
                        error = await delete.json()
                        raise ClientConnectionError(error)
        except ClientConnectionError as e:
            logging.warning(f"Api error: {self._link}{route} {e}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")
