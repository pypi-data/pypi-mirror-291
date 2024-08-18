"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*
Copyright 2020 Alibaba Group Holding Limited.

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
import groot.sdk.client_backup_service_pb2
import grpc
import grpc.aio
import typing

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class ClientBackupStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    createNewGraphBackup: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.CreateNewGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.CreateNewGraphBackupResponse,
    ]

    deleteGraphBackup: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.DeleteGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.DeleteGraphBackupResponse,
    ]

    purgeOldGraphBackups: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsRequest,
        groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsResponse,
    ]

    restoreFromGraphBackup: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupResponse,
    ]

    verifyGraphBackup: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.VerifyGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.VerifyGraphBackupResponse,
    ]

    getGraphBackupInfo: grpc.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.GetGraphBackupInfoRequest,
        groot.sdk.client_backup_service_pb2.GetGraphBackupInfoResponse,
    ]

class ClientBackupAsyncStub:
    createNewGraphBackup: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.CreateNewGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.CreateNewGraphBackupResponse,
    ]

    deleteGraphBackup: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.DeleteGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.DeleteGraphBackupResponse,
    ]

    purgeOldGraphBackups: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsRequest,
        groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsResponse,
    ]

    restoreFromGraphBackup: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupResponse,
    ]

    verifyGraphBackup: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.VerifyGraphBackupRequest,
        groot.sdk.client_backup_service_pb2.VerifyGraphBackupResponse,
    ]

    getGraphBackupInfo: grpc.aio.UnaryUnaryMultiCallable[
        groot.sdk.client_backup_service_pb2.GetGraphBackupInfoRequest,
        groot.sdk.client_backup_service_pb2.GetGraphBackupInfoResponse,
    ]

class ClientBackupServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createNewGraphBackup(
        self,
        request: groot.sdk.client_backup_service_pb2.CreateNewGraphBackupRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.CreateNewGraphBackupResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.CreateNewGraphBackupResponse]]: ...

    @abc.abstractmethod
    def deleteGraphBackup(
        self,
        request: groot.sdk.client_backup_service_pb2.DeleteGraphBackupRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.DeleteGraphBackupResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.DeleteGraphBackupResponse]]: ...

    @abc.abstractmethod
    def purgeOldGraphBackups(
        self,
        request: groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.PurgeOldGraphBackupsResponse]]: ...

    @abc.abstractmethod
    def restoreFromGraphBackup(
        self,
        request: groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.RestoreFromGraphBackupResponse]]: ...

    @abc.abstractmethod
    def verifyGraphBackup(
        self,
        request: groot.sdk.client_backup_service_pb2.VerifyGraphBackupRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.VerifyGraphBackupResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.VerifyGraphBackupResponse]]: ...

    @abc.abstractmethod
    def getGraphBackupInfo(
        self,
        request: groot.sdk.client_backup_service_pb2.GetGraphBackupInfoRequest,
        context: _ServicerContext,
    ) -> typing.Union[groot.sdk.client_backup_service_pb2.GetGraphBackupInfoResponse, collections.abc.Awaitable[groot.sdk.client_backup_service_pb2.GetGraphBackupInfoResponse]]: ...

def add_ClientBackupServicer_to_server(servicer: ClientBackupServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
