# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from groot.sdk import client_backup_service_pb2 as groot_dot_sdk_dot_client__backup__service__pb2

GRPC_GENERATED_VERSION = '1.65.5'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.66.0'
SCHEDULED_RELEASE_DATE = 'August 6, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in groot/sdk/client_backup_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ClientBackupStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.createNewGraphBackup = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/createNewGraphBackup',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupResponse.FromString,
                _registered_method=True)
        self.deleteGraphBackup = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/deleteGraphBackup',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupResponse.FromString,
                _registered_method=True)
        self.purgeOldGraphBackups = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/purgeOldGraphBackups',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsResponse.FromString,
                _registered_method=True)
        self.restoreFromGraphBackup = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/restoreFromGraphBackup',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupResponse.FromString,
                _registered_method=True)
        self.verifyGraphBackup = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/verifyGraphBackup',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupResponse.FromString,
                _registered_method=True)
        self.getGraphBackupInfo = channel.unary_unary(
                '/gs.rpc.groot.ClientBackup/getGraphBackupInfo',
                request_serializer=groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoResponse.FromString,
                _registered_method=True)


class ClientBackupServicer(object):
    """Missing associated documentation comment in .proto file."""

    def createNewGraphBackup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteGraphBackup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def purgeOldGraphBackups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def restoreFromGraphBackup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verifyGraphBackup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getGraphBackupInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientBackupServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'createNewGraphBackup': grpc.unary_unary_rpc_method_handler(
                    servicer.createNewGraphBackup,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupResponse.SerializeToString,
            ),
            'deleteGraphBackup': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteGraphBackup,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupResponse.SerializeToString,
            ),
            'purgeOldGraphBackups': grpc.unary_unary_rpc_method_handler(
                    servicer.purgeOldGraphBackups,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsResponse.SerializeToString,
            ),
            'restoreFromGraphBackup': grpc.unary_unary_rpc_method_handler(
                    servicer.restoreFromGraphBackup,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupResponse.SerializeToString,
            ),
            'verifyGraphBackup': grpc.unary_unary_rpc_method_handler(
                    servicer.verifyGraphBackup,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupResponse.SerializeToString,
            ),
            'getGraphBackupInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.getGraphBackupInfo,
                    request_deserializer=groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gs.rpc.groot.ClientBackup', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gs.rpc.groot.ClientBackup', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ClientBackup(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def createNewGraphBackup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/createNewGraphBackup',
            groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.CreateNewGraphBackupResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def deleteGraphBackup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/deleteGraphBackup',
            groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.DeleteGraphBackupResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def purgeOldGraphBackups(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/purgeOldGraphBackups',
            groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.PurgeOldGraphBackupsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def restoreFromGraphBackup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/restoreFromGraphBackup',
            groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.RestoreFromGraphBackupResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def verifyGraphBackup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/verifyGraphBackup',
            groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.VerifyGraphBackupResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getGraphBackupInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientBackup/getGraphBackupInfo',
            groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoRequest.SerializeToString,
            groot_dot_sdk_dot_client__backup__service__pb2.GetGraphBackupInfoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
