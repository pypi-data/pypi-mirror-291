# pylint: disable=unused-argument
from .fakers import (
    initialize_db,
)
from .types import (
    AsyncGeneratorFixture,
    DynamoDBResource,
    FunctionCallsStore,
    FunctionFixture,
    GeneratorFixture,
    MockingFunction,
    MockingValue,
    Patch,
    SetupFixture,
)
import aioboto3 as _aioboto3
from aiobotocore.config import (
    AioConfig,
)
import boto3 as _boto3
import moto as _moto
from moto.server import (
    ThreadedMotoServer,
)
import os as _os
import pytest as _pytest
import pytest_asyncio as _pytest_asyncio
from unittest.mock import (
    patch,
)


class CustomFixturesPlugin:
    @_pytest.fixture(autouse=True)
    def aws_credentials(self) -> SetupFixture:
        """Mocked AWS Credentials for moto."""
        _os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        _os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        _os.environ["AWS_SECURITY_TOKEN"] = "testing"
        _os.environ["AWS_SESSION_TOKEN"] = "testing"
        _os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    @_pytest.fixture(scope="function")
    def moto_session(self) -> GeneratorFixture[None]:
        """Starts the moto server and mocks the boto3 and aioboto3 sessions."""
        mocked_boto = _moto.mock_aws()
        mocked_boto.start()
        yield
        mocked_boto.stop()

    @_pytest.fixture(scope="function")
    def async_moto_session(self) -> GeneratorFixture[str]:
        """Starts the moto server and mocks the boto3 and aioboto3 sessions."""
        aio_session = _aioboto3.Session()

        sessions: list[Patch] = [
            patch("aioboto3.Session", lambda: aio_session),
            patch("aioboto3.session.Session", lambda: aio_session),
        ]

        server = ThreadedMotoServer(port=8022)
        server.start()
        host, port = server.get_host_and_port()

        for session in sessions:
            session.start()

        yield f"http://{host}:{port}"

        for session in sessions:
            session.stop()

        server.stop()

    @_pytest.fixture(scope="function")
    def dynamodb_resource(
        self, moto_session: GeneratorFixture[None]
    ) -> GeneratorFixture[DynamoDBResource]:
        """Returns a DynamoDB service resource with example table
        for testing purposes.
        """
        session = _boto3.Session()
        resource = session.resource(service_name="dynamodb")
        initialize_db(resource)
        yield resource

    @_pytest_asyncio.fixture(scope="function")
    async def async_dynamodb_resource(
        self,
        async_moto_session: str,
    ) -> AsyncGeneratorFixture[DynamoDBResource]:
        """Returns a DynamoDB service resource from aioboto3 with example table
        for testing purposes.
        """

        session = _aioboto3.Session()
        config = AioConfig(
            connect_timeout=10,
            max_pool_connections=0,
            read_timeout=5,
            retries={"max_attempts": 10, "mode": "standard"},
        )
        async with session.resource(
            endpoint_url=async_moto_session,
            service_name="dynamodb",
            config=config,
        ) as resource:
            await initialize_db(resource)
            yield resource

    @_pytest.fixture(scope="function")
    def patch_table(
        self, dynamodb_resource: DynamoDBResource
    ) -> FunctionFixture[Patch]:
        """Change a DynamoDB table resource variable with a
        mocked table resource.
        """

        def _mock_table(
            module: object, resource: str, table_name: str
        ) -> Patch:
            table = dynamodb_resource.Table(table_name)
            return patch.object(module, resource, table)

        return _mock_table

    @_pytest.fixture(scope="function")
    def mocking(self, monkeypatch: _pytest.MonkeyPatch) -> MockingFunction:
        store = FunctionCallsStore()

        def _mock(
            module: object, method: str, result: object
        ) -> FunctionCallsStore:
            def _mocked(*args: tuple, **kwargs: dict) -> object:
                store.append_call(args, kwargs, result)
                return result

            monkeypatch.setattr(module, method, _mocked)
            return store

        return _mock

    @_pytest.fixture(scope="function")
    def value_mocking(self, monkeypatch: _pytest.MonkeyPatch) -> MockingValue:
        def _mock(module: object, method: str, result: object) -> None:
            monkeypatch.setattr(module, method, result)

        return _mock

    @_pytest.fixture(scope="function")
    def async_mocking(
        self, monkeypatch: _pytest.MonkeyPatch
    ) -> MockingFunction:
        store = FunctionCallsStore()

        def _mock(
            module: object, method: str, result: object
        ) -> FunctionCallsStore:
            async def _mocked(*args: tuple, **kwargs: dict) -> object:
                store.append_call(args, kwargs, result)
                return result

            monkeypatch.setattr(module, method, _mocked)
            return store

        return _mock
