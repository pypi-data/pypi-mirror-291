import io
import typing
import warnings

import httpx
from typing_extensions import TypeVar, ParamSpec

from .base_client import BaseAthena, AsyncBaseAthena
from .environment import AthenaEnvironment
from .polling_message_client import MessagePollingClient, AsyncMessagePollingClient
from .tools.client import AsyncToolsClient, ToolsClient
from .types.data_frame_request_out import DataFrameRequestOut

if typing.TYPE_CHECKING:
    import pandas as pd


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar('U')


def _inherit_signature(f: typing.Callable[P, T]) -> typing.Callable[..., typing.Callable[P, U]]:
    return lambda x: x


class WrappedToolsClient(ToolsClient):

    def get_file(self, document_id: str) -> io.BytesIO:
        file_bytes = b''.join(self.raw_data(document_id=document_id))
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature(ToolsClient.data_frame)
    def data_frame(self, *, document_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = super().data_frame(document_id=document_id, **kwargs)
        return _read_json_frame(model)

    def read_data_frame(self, document_id: str, *args, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        file_bytes = self.get_file(document_id)
        return _to_pandas_df(file_bytes, *args, **kwargs)


class WrappedAsyncToolsClient(AsyncToolsClient):

    async def get_file(self, document_id: str) -> io.BytesIO:
        file_bytes = b''.join([gen async for gen in self.raw_data(document_id=document_id)])
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature(ToolsClient.data_frame)
    async def data_frame(self, *, document_id: str, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        model = await super().data_frame(document_id=document_id, **kwargs)
        return _read_json_frame(model)

    async def read_data_frame(self, document_id: str, *args, **kwargs) -> 'pd.DataFrame':
        _check_pandas_installed()
        file_bytes = await self.get_file(document_id)
        return _to_pandas_df(file_bytes, *args, **kwargs)


class Athena(BaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: AthenaEnvironment. The environment to use for requests from the client. from .environment import AthenaEnvironment

                                          Defaults to AthenaEnvironment.DEFAULT

        - api_key: str.

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from athena.client import Athena

    client = Athena(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: AthenaEnvironment = AthenaEnvironment.DEFAULT,
        api_key: str,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )
        self.message = MessagePollingClient(
            client_wrapper=self._client_wrapper)
        self.tools = WrappedToolsClient(client_wrapper=self._client_wrapper)


class AsyncAthena(AsyncBaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: AthenaEnvironment. The environment to use for requests from the client. from .environment import AthenaEnvironment

                                          Defaults to AthenaEnvironment.DEFAULT

        - api_key: str.

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from athena.client import AsyncAthena

    client = AsyncAthena(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: AthenaEnvironment = AthenaEnvironment.DEFAULT,
        api_key: str,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )
        self.message = AsyncMessagePollingClient(
            client_wrapper=self._client_wrapper)
        self.tools = WrappedAsyncToolsClient(client_wrapper=self._client_wrapper)


def _read_json_frame(model: DataFrameRequestOut) -> 'pd.DataFrame':
    import pandas as pd

    string_io = io.StringIO(model.json())

    with warnings.catch_warnings():
        # Filter warnings due to https://github.com/pandas-dev/pandas/issues/59511
        warnings.simplefilter(action='ignore', category=FutureWarning)
        return pd.read_json(string_io, orient='split')


def _check_pandas_installed():
    import pandas
    assert pandas


def _to_pandas_df(bytes_io: io.BytesIO, *args, **kwargs):
    import pandas as pd
    import magic

    # ideally this would be read from response header, but fern SDK for Python hides this info from us
    media_type = magic.from_buffer(bytes_io.read(2048), mime=True)
    bytes_io.seek(0)

    if media_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return pd.read_excel(bytes_io, *args, engine='openpyxl', **kwargs)
    elif media_type == 'application/vnd.ms-excel':
        return pd.read_excel(bytes_io, *args, **kwargs)
    elif media_type == 'text/csv':
        return pd.read_csv(bytes_io, *args, **kwargs)
    else:
        raise Exception("Unknown media type")
