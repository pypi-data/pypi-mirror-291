# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import write_service_pb2 as write__service__pb2

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
        + f' but the generated code in write_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ClientWriteStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getClientId = channel.unary_unary(
                '/gs.rpc.groot.ClientWrite/getClientId',
                request_serializer=write__service__pb2.GetClientIdRequest.SerializeToString,
                response_deserializer=write__service__pb2.GetClientIdResponse.FromString,
                _registered_method=True)
        self.batchWrite = channel.unary_unary(
                '/gs.rpc.groot.ClientWrite/batchWrite',
                request_serializer=write__service__pb2.BatchWriteRequest.SerializeToString,
                response_deserializer=write__service__pb2.BatchWriteResponse.FromString,
                _registered_method=True)
        self.remoteFlush = channel.unary_unary(
                '/gs.rpc.groot.ClientWrite/remoteFlush',
                request_serializer=write__service__pb2.RemoteFlushRequest.SerializeToString,
                response_deserializer=write__service__pb2.RemoteFlushResponse.FromString,
                _registered_method=True)
        self.replayRecords = channel.unary_unary(
                '/gs.rpc.groot.ClientWrite/replayRecords',
                request_serializer=write__service__pb2.ReplayRecordsRequest.SerializeToString,
                response_deserializer=write__service__pb2.ReplayRecordsResponse.FromString,
                _registered_method=True)


class ClientWriteServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getClientId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def batchWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remoteFlush(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def replayRecords(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientWriteServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getClientId': grpc.unary_unary_rpc_method_handler(
                    servicer.getClientId,
                    request_deserializer=write__service__pb2.GetClientIdRequest.FromString,
                    response_serializer=write__service__pb2.GetClientIdResponse.SerializeToString,
            ),
            'batchWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.batchWrite,
                    request_deserializer=write__service__pb2.BatchWriteRequest.FromString,
                    response_serializer=write__service__pb2.BatchWriteResponse.SerializeToString,
            ),
            'remoteFlush': grpc.unary_unary_rpc_method_handler(
                    servicer.remoteFlush,
                    request_deserializer=write__service__pb2.RemoteFlushRequest.FromString,
                    response_serializer=write__service__pb2.RemoteFlushResponse.SerializeToString,
            ),
            'replayRecords': grpc.unary_unary_rpc_method_handler(
                    servicer.replayRecords,
                    request_deserializer=write__service__pb2.ReplayRecordsRequest.FromString,
                    response_serializer=write__service__pb2.ReplayRecordsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gs.rpc.groot.ClientWrite', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gs.rpc.groot.ClientWrite', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ClientWrite(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getClientId(request,
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
            '/gs.rpc.groot.ClientWrite/getClientId',
            write__service__pb2.GetClientIdRequest.SerializeToString,
            write__service__pb2.GetClientIdResponse.FromString,
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
    def batchWrite(request,
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
            '/gs.rpc.groot.ClientWrite/batchWrite',
            write__service__pb2.BatchWriteRequest.SerializeToString,
            write__service__pb2.BatchWriteResponse.FromString,
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
    def remoteFlush(request,
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
            '/gs.rpc.groot.ClientWrite/remoteFlush',
            write__service__pb2.RemoteFlushRequest.SerializeToString,
            write__service__pb2.RemoteFlushResponse.FromString,
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
    def replayRecords(request,
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
            '/gs.rpc.groot.ClientWrite/replayRecords',
            write__service__pb2.ReplayRecordsRequest.SerializeToString,
            write__service__pb2.ReplayRecordsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
