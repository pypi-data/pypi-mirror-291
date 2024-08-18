"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*

The file proto/attr_value.proto is referred and derived from project
tensorflow,

   https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/framework/attr_value.proto

which has the following license:


Copyright 2015 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Code:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Code.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    OK: _Code.ValueType  # 0
    """Not an error; returned on success."""
    CANCELLED: _Code.ValueType  # 1
    INVALID_ARGUMENT: _Code.ValueType  # 2
    """Arguments of operations is invalid / in a wrong format."""
    TIMEOUT: _Code.ValueType  # 3
    """Timeout, used when an operation fail to return result in an specific time."""
    NOT_FOUND: _Code.ValueType  # 4
    """Required resources cannot be found."""
    ALREADY_EXISTS: _Code.ValueType  # 5
    """File or resources already existed."""
    RESOURCE_EXHAUSTED: _Code.ValueType  # 6
    UNIMPLEMENTED: _Code.ValueType  # 7
    """Functionality not implemented yet"""
    PERMISSION_DENIED: _Code.ValueType  # 8
    """Client doesn't have the permission."""
    COMPILATION_FAILURE: _Code.ValueType  # 9
    """Compile graph frame or app frame failed."""
    PORT_IN_USE: _Code.ValueType  # 10
    UNSUPPORTED_OPERATION: _Code.ValueType  # 11
    ILLEGAL_STATE: _Code.ValueType  # 12
    NETWORK_FAILURE: _Code.ValueType  # 13
    """Network is unreachable"""
    CODEGEN_ERROR: _Code.ValueType  # 100
    """InValidArgument = 100;
    UnsupportedOperator = 101;
    AlreadyExists = 102;
    NotExists = 103;
    CodegenError = 100;
    UninitializedStatus = 101;
    """
    INVALID_SCHEMA: _Code.ValueType  # 101
    """InvalidSchema = 101;"""
    ILLEGAL_OPERATION: _Code.ValueType  # 102
    """PermissionError = 107;
    IllegalOperation = 102;
    """
    INTERNAL_ERROR: _Code.ValueType  # 103
    """InternalError = 103;"""
    INVALID_IMPORT_FILE: _Code.ValueType  # 104
    """InvalidImportFile = 104;"""
    IO_ERROR: _Code.ValueType  # 105
    """IOError = 105;"""
    QUERY_FAILED: _Code.ValueType  # 106
    """NotFound = 112;
    QueryFailed = 106;
    """
    REOPEN_ERROR: _Code.ValueType  # 107
    """ReopenError = 107;"""
    ERROR_OPEN_META: _Code.ValueType  # 108
    """ErrorOpenMeta = 108;"""
    SQL_EXECUTION_ERROR: _Code.ValueType  # 109
    """SQlExecutionError = 109;"""
    SQL_BINDING_ERROR: _Code.ValueType  # 110
    """SqlBindingError = 110;"""
    ALREADY_LOCKED: _Code.ValueType  # 111
    """Unimplemented = 118;
    AlreadyLocked = 111;
    """

class Code(_Code, metaclass=_CodeEnumTypeWrapper):
    """component-05: GIE Interactive Server (flex)"""

OK: Code.ValueType  # 0
"""Not an error; returned on success."""
CANCELLED: Code.ValueType  # 1
INVALID_ARGUMENT: Code.ValueType  # 2
"""Arguments of operations is invalid / in a wrong format."""
TIMEOUT: Code.ValueType  # 3
"""Timeout, used when an operation fail to return result in an specific time."""
NOT_FOUND: Code.ValueType  # 4
"""Required resources cannot be found."""
ALREADY_EXISTS: Code.ValueType  # 5
"""File or resources already existed."""
RESOURCE_EXHAUSTED: Code.ValueType  # 6
UNIMPLEMENTED: Code.ValueType  # 7
"""Functionality not implemented yet"""
PERMISSION_DENIED: Code.ValueType  # 8
"""Client doesn't have the permission."""
COMPILATION_FAILURE: Code.ValueType  # 9
"""Compile graph frame or app frame failed."""
PORT_IN_USE: Code.ValueType  # 10
UNSUPPORTED_OPERATION: Code.ValueType  # 11
ILLEGAL_STATE: Code.ValueType  # 12
NETWORK_FAILURE: Code.ValueType  # 13
"""Network is unreachable"""
CODEGEN_ERROR: Code.ValueType  # 100
"""InValidArgument = 100;
UnsupportedOperator = 101;
AlreadyExists = 102;
NotExists = 103;
CodegenError = 100;
UninitializedStatus = 101;
"""
INVALID_SCHEMA: Code.ValueType  # 101
"""InvalidSchema = 101;"""
ILLEGAL_OPERATION: Code.ValueType  # 102
"""PermissionError = 107;
IllegalOperation = 102;
"""
INTERNAL_ERROR: Code.ValueType  # 103
"""InternalError = 103;"""
INVALID_IMPORT_FILE: Code.ValueType  # 104
"""InvalidImportFile = 104;"""
IO_ERROR: Code.ValueType  # 105
"""IOError = 105;"""
QUERY_FAILED: Code.ValueType  # 106
"""NotFound = 112;
QueryFailed = 106;
"""
REOPEN_ERROR: Code.ValueType  # 107
"""ReopenError = 107;"""
ERROR_OPEN_META: Code.ValueType  # 108
"""ErrorOpenMeta = 108;"""
SQL_EXECUTION_ERROR: Code.ValueType  # 109
"""SQlExecutionError = 109;"""
SQL_BINDING_ERROR: Code.ValueType  # 110
"""SqlBindingError = 110;"""
ALREADY_LOCKED: Code.ValueType  # 111
"""Unimplemented = 118;
AlreadyLocked = 111;
"""
global___Code = Code
