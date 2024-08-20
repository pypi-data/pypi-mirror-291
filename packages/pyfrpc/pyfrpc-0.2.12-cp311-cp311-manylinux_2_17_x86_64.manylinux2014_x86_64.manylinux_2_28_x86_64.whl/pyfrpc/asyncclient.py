# -*- coding: utf-8 -*-

import ssl
import xmlrpc.client
from typing import Any, Dict, Optional, Sequence, Tuple

import aiohttp

from .client import _FrpcClientAttr
from .coding import decode, encode
from .models import FrpcCall, FrpcFault, FrpcResponse

APPLICATION_FRPC = "application/x-frpc"


class AsyncFrpcClient:
    def __init__(
        self,
        url: str,
        *,
        cert: Optional[Tuple[str,str]] = None,
        verify: bool = True,
        timeout: float = 60.0,
        session: Optional[aiohttp.ClientSession] = None,
        version: int = 0x0201,
        req_opts: Optional[Dict[str, Any]] = None
    ) -> None:
        self._url = url
        self._version = version

        if session:
            self.session = session
        else:
            connector = None

            sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)

            if not verify:
                sslcontext.verify_flags = 0

            if cert:
                sslcontext.load_cert_chain(certfile=cert[0], keyfile=cert[1])

            connector = aiohttp.TCPConnector(ssl_context=sslcontext)

            jar = aiohttp.DummyCookieJar()
            self.session = aiohttp.ClientSession(cookie_jar=jar, connector=connector)

        self._opts = req_opts or {}
        self._opts.setdefault("timeout", timeout)

    async def call(
        self,
        method: str,
        args: Sequence[Any] = (),
        **kwargs
    ) -> Any:
        payload = encode(FrpcCall(name=method, args=args), self._version)

        headers = kwargs.pop('headers', {})
        headers.update({
            "Content-Type" : APPLICATION_FRPC,
            "Accept" : APPLICATION_FRPC,
        })

        for k,v in self._opts.items():
            kwargs.setdefault(k, v)

        async with self.session.post(url=self._url, data=payload, headers=headers, **kwargs) as res:
            if res.status != 200:
                raise RuntimeError("bad status code, expected 200, got {:d}".format(res.status))

            content = await res.read()
            content_type = res.headers.get("Content-Type", None)

        # FRPC decoding
        if content_type == APPLICATION_FRPC:
            payload = decode(content)

            if isinstance(payload, FrpcFault):
                raise payload

            return payload.data

        # XML-RPC decoding
        if content_type == "text/xml":
            try:
                payload, _ = xmlrpc.client.loads(
                    content, use_datetime=True, use_builtin_types=True)
                return payload[0]
            except xmlrpc.client.Fault as e:
                raise FrpcFault(e.faultCode, e.faultString)

        raise RuntimeError("bad content type: " + content_type)

    async def close(self) -> None:
        await self.session.close()

    async def __aenter__(self) -> "AsyncFrpcClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    @property
    def rpc(self) -> _FrpcClientAttr:
        return _FrpcClientAttr(self, "")

    @property
    def url(self) -> str:
        return self._url


class _AsyncFrpcClientAttr(object):
    def __init__(self,
        client: AsyncFrpcClient,
        method: str
    ):
        self._client = client
        self._method = method

        self._prefix = self._method + ("." if self._method else "")

    def __getattr__(self, name: str) -> "_AsyncFrpcClientAttr":
        if name.startswith("__"):
            return super().__getattr__(name)

        method = self._prefix + name
        return _FrpcClientAttr(self._client, method)

    async def __call__(self, *args, **kwargs):
        return await self._client.call(self._method, args, **kwargs)
