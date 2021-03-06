# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rpc.proto',
  package='thirdparty.public.protobuf.socketrpc',
  serialized_pb='\n\trpc.proto\x12$thirdparty.public.protobuf.socketrpc\"K\n\x07Request\x12\x14\n\x0cservice_name\x18\x01 \x02(\t\x12\x13\n\x0bmethod_name\x18\x02 \x02(\t\x12\x15\n\rrequest_proto\x18\x03 \x02(\x0c\"\x93\x01\n\x08Response\x12\x16\n\x0eresponse_proto\x18\x01 \x01(\x0c\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x12\x17\n\x08\x63\x61llback\x18\x03 \x01(\x08:\x05\x66\x61lse\x12G\n\x0c\x65rror_reason\x18\x04 \x01(\x0e\x32\x31.thirdparty.public.protobuf.socketrpc.ErrorReason*\xd9\x01\n\x0b\x45rrorReason\x12\x14\n\x10\x42\x41\x44_REQUEST_DATA\x10\x00\x12\x15\n\x11\x42\x41\x44_REQUEST_PROTO\x10\x01\x12\x15\n\x11SERVICE_NOT_FOUND\x10\x02\x12\x14\n\x10METHOD_NOT_FOUND\x10\x03\x12\r\n\tRPC_ERROR\x10\x04\x12\x0e\n\nRPC_FAILED\x10\x05\x12\x19\n\x15INVALID_REQUEST_PROTO\x10\x06\x12\x16\n\x12\x42\x41\x44_RESPONSE_PROTO\x10\x07\x12\x10\n\x0cUNKNOWN_HOST\x10\x08\x12\x0c\n\x08IO_ERROR\x10\tB4\n!com.googlecode.protobuf.socketrpcB\x0fSocketRpcProtos')

_ERRORREASON = _descriptor.EnumDescriptor(
  name='ErrorReason',
  full_name='thirdparty.public.protobuf.socketrpc.ErrorReason',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST_DATA', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST_PROTO', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVICE_NOT_FOUND', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='METHOD_NOT_FOUND', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RPC_ERROR', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RPC_FAILED', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REQUEST_PROTO', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BAD_RESPONSE_PROTO', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_HOST', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IO_ERROR', index=9, number=9,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=279,
  serialized_end=496,
)

ErrorReason = enum_type_wrapper.EnumTypeWrapper(_ERRORREASON)
BAD_REQUEST_DATA = 0
BAD_REQUEST_PROTO = 1
SERVICE_NOT_FOUND = 2
METHOD_NOT_FOUND = 3
RPC_ERROR = 4
RPC_FAILED = 5
INVALID_REQUEST_PROTO = 6
BAD_RESPONSE_PROTO = 7
UNKNOWN_HOST = 8
IO_ERROR = 9



_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='thirdparty.public.protobuf.socketrpc.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='service_name', full_name='thirdparty.public.protobuf.socketrpc.Request.service_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method_name', full_name='thirdparty.public.protobuf.socketrpc.Request.method_name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_proto', full_name='thirdparty.public.protobuf.socketrpc.Request.request_proto', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=51,
  serialized_end=126,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='thirdparty.public.protobuf.socketrpc.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response_proto', full_name='thirdparty.public.protobuf.socketrpc.Response.response_proto', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='thirdparty.public.protobuf.socketrpc.Response.error', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='callback', full_name='thirdparty.public.protobuf.socketrpc.Response.callback', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_reason', full_name='thirdparty.public.protobuf.socketrpc.Response.error_reason', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=129,
  serialized_end=276,
)

_RESPONSE.fields_by_name['error_reason'].enum_type = _ERRORREASON
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE

class Request(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST

  # @@protoc_insertion_point(class_scope:thirdparty.public.protobuf.socketrpc.Request)

class Response(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSE

  # @@protoc_insertion_point(class_scope:thirdparty.public.protobuf.socketrpc.Response)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\n!com.googlecode.protobuf.socketrpcB\017SocketRpcProtos')
# @@protoc_insertion_point(module_scope)
