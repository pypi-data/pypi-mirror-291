"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import abc
import collections.abc
import ddl_service_pb2
import grpc
import grpc.aio
import typing

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class GrootDdlServiceStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    batchSubmit: grpc.UnaryUnaryMultiCallable[
        ddl_service_pb2.BatchSubmitRequest,
        ddl_service_pb2.BatchSubmitResponse,
    ]

    getGraphDef: grpc.UnaryUnaryMultiCallable[
        ddl_service_pb2.GetGraphDefRequest,
        ddl_service_pb2.GetGraphDefResponse,
    ]

class GrootDdlServiceAsyncStub:
    batchSubmit: grpc.aio.UnaryUnaryMultiCallable[
        ddl_service_pb2.BatchSubmitRequest,
        ddl_service_pb2.BatchSubmitResponse,
    ]

    getGraphDef: grpc.aio.UnaryUnaryMultiCallable[
        ddl_service_pb2.GetGraphDefRequest,
        ddl_service_pb2.GetGraphDefResponse,
    ]

class GrootDdlServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def batchSubmit(
        self,
        request: ddl_service_pb2.BatchSubmitRequest,
        context: _ServicerContext,
    ) -> typing.Union[ddl_service_pb2.BatchSubmitResponse, collections.abc.Awaitable[ddl_service_pb2.BatchSubmitResponse]]: ...

    @abc.abstractmethod
    def getGraphDef(
        self,
        request: ddl_service_pb2.GetGraphDefRequest,
        context: _ServicerContext,
    ) -> typing.Union[ddl_service_pb2.GetGraphDefResponse, collections.abc.Awaitable[ddl_service_pb2.GetGraphDefResponse]]: ...

def add_GrootDdlServiceServicer_to_server(servicer: GrootDdlServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
