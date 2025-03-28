#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,utf8 strings
#

from ...thrift.Thrift import TType, TMessageType, TException, TApplicationException

from ...thrift.transport import TTransport
from ...thrift.protocol import TBinaryProtocol, TProtocol

try:
    from ...thrift.protocol import fastbinary
except:
    fastbinary = None


class EDAMErrorCode(object):
    """
    Numeric codes indicating the type of error that occurred on the
    service.
    <dl>
      <dt>UNKNOWN</dt>
        <dd>No information available about the error</dd>
      <dt>BAD_DATA_FORMAT</dt>
        <dd>The format of the request data was incorrect</dd>
      <dt>PERMISSION_DENIED</dt>
        <dd>Not permitted to perform action</dd>
      <dt>INTERNAL_ERROR</dt>
        <dd>Unexpected problem with the service</dd>
      <dt>DATA_REQUIRED</dt>
        <dd>A required parameter/field was absent</dd>
      <dt>LIMIT_REACHED</dt>
        <dd>Operation denied due to data model limit</dd>
      <dt>QUOTA_REACHED</dt>
        <dd>Operation denied due to user storage limit</dd>
      <dt>INVALID_AUTH</dt>
        <dd>Username and/or password incorrect</dd>
      <dt>AUTH_EXPIRED</dt>
        <dd>Authentication token expired</dd>
      <dt>DATA_CONFLICT</dt>
        <dd>Change denied due to data model conflict</dd>
      <dt>ENML_VALIDATION</dt>
        <dd>Content of submitted note was malformed</dd>
      <dt>SHARD_UNAVAILABLE</dt>
        <dd>Service shard with account data is temporarily down</dd>
      <dt>LEN_TOO_SHORT</dt>
        <dd>Operation denied due to data model limit, where something such
            as a string length was too short</dd>
      <dt>LEN_TOO_LONG</dt>
        <dd>Operation denied due to data model limit, where something such
            as a string length was too long</dd>
      <dt>TOO_FEW</dt>
        <dd>Operation denied due to data model limit, where there were
            too few of something.</dd>
      <dt>TOO_MANY</dt>
        <dd>Operation denied due to data model limit, where there were
            too many of something.</dd>
      <dt>UNSUPPORTED_OPERATION</dt>
        <dd>Operation denied because it is currently unsupported.</dd>
      <dt>TAKEN_DOWN</dt>
        <dd>Operation denied because access to the corresponding object is
            prohibited in response to a take-down notice.</dd>
      <dt>RATE_LIMIT_REACHED</dt>
        <dd>Operation denied because the calling application has reached
            its hourly API call limit for this user.</dd>
    </dl>
    """
    UNKNOWN = 1
    BAD_DATA_FORMAT = 2
    PERMISSION_DENIED = 3
    INTERNAL_ERROR = 4
    DATA_REQUIRED = 5
    LIMIT_REACHED = 6
    QUOTA_REACHED = 7
    INVALID_AUTH = 8
    AUTH_EXPIRED = 9
    DATA_CONFLICT = 10
    ENML_VALIDATION = 11
    SHARD_UNAVAILABLE = 12
    LEN_TOO_SHORT = 13
    LEN_TOO_LONG = 14
    TOO_FEW = 15
    TOO_MANY = 16
    UNSUPPORTED_OPERATION = 17
    TAKEN_DOWN = 18
    RATE_LIMIT_REACHED = 19

    _VALUES_TO_NAMES = {
        1: "UNKNOWN",
        2: "BAD_DATA_FORMAT",
        3: "PERMISSION_DENIED",
        4: "INTERNAL_ERROR",
        5: "DATA_REQUIRED",
        6: "LIMIT_REACHED",
        7: "QUOTA_REACHED",
        8: "INVALID_AUTH",
        9: "AUTH_EXPIRED",
        10: "DATA_CONFLICT",
        11: "ENML_VALIDATION",
        12: "SHARD_UNAVAILABLE",
        13: "LEN_TOO_SHORT",
        14: "LEN_TOO_LONG",
        15: "TOO_FEW",
        16: "TOO_MANY",
        17: "UNSUPPORTED_OPERATION",
        18: "TAKEN_DOWN",
        19: "RATE_LIMIT_REACHED",
    }

    _NAMES_TO_VALUES = {
        "UNKNOWN": 1,
        "BAD_DATA_FORMAT": 2,
        "PERMISSION_DENIED": 3,
        "INTERNAL_ERROR": 4,
        "DATA_REQUIRED": 5,
        "LIMIT_REACHED": 6,
        "QUOTA_REACHED": 7,
        "INVALID_AUTH": 8,
        "AUTH_EXPIRED": 9,
        "DATA_CONFLICT": 10,
        "ENML_VALIDATION": 11,
        "SHARD_UNAVAILABLE": 12,
        "LEN_TOO_SHORT": 13,
        "LEN_TOO_LONG": 14,
        "TOO_FEW": 15,
        "TOO_MANY": 16,
        "UNSUPPORTED_OPERATION": 17,
        "TAKEN_DOWN": 18,
        "RATE_LIMIT_REACHED": 19,
    }


class EDAMUserException(TException):
    """
    This exception is thrown by EDAM procedures when a call fails as a result of
    a problem that a caller may be able to resolve.  For example, if the user
    attempts to add a note to their account which would exceed their storage
    quota, this type of exception may be thrown to indicate the source of the
    error so that they can choose an alternate action.

    This exception would not be used for internal system errors that do not
    reflect user actions, but rather reflect a problem within the service that
    the user cannot resolve.

    errorCode:  The numeric code indicating the type of error that occurred.
      must be one of the values of EDAMErrorCode.

    parameter:  If the error applied to a particular input parameter, this will
      indicate which parameter.

    Attributes:
     - errorCode
     - parameter
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'errorCode', None, None,),  # 1
        (2, TType.STRING, 'parameter', None, None,),  # 2
    )

    def __init__(self, errorCode=None, parameter=None, ):
        self.errorCode = errorCode
        self.parameter = parameter

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.errorCode = iprot.readI32();
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.parameter = iprot.readString().decode('utf-8')
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('EDAMUserException')
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 1)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.parameter is not None:
            oprot.writeFieldBegin('parameter', TType.STRING, 2)
            oprot.writeString(self.parameter.encode('utf-8'))
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.errorCode is None:
            raise TProtocol.TProtocolException(message='Required field errorCode is unset!')
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class EDAMSystemException(TException):
    """
    This exception is thrown by EDAM procedures when a call fails as a result of
    a problem in the service that could not be changed through caller action.

    errorCode:  The numeric code indicating the type of error that occurred.
      must be one of the values of EDAMErrorCode.

    message:  This may contain additional information about the error

    rateLimitDuration:  Indicates the minimum number of seconds that an application should
      expect subsequent API calls for this user to fail. The application should not retry
      API requests for the user until at least this many seconds have passed. Present only
      when errorCode is RATE_LIMIT_REACHED,

    Attributes:
     - errorCode
     - message
     - rateLimitDuration
    """
    thrift_spec = (
        None,  # 0
        (1, TType.I32, 'errorCode', None, None,),  # 1
        (2, TType.STRING, 'message', None, None,),  # 2
        (3, TType.I32, 'rateLimitDuration', None, None,),  # 3
    )

    def __init__(self, errorCode=None, message=None, rateLimitDuration=None, ):
        TException.__init__(self, message)
        self.errorCode = errorCode
        self.message = message
        self.rateLimitDuration = rateLimitDuration

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.errorCode = iprot.readI32();
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8')
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.rateLimitDuration = iprot.readI32();
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('EDAMSystemException')
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 1)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message.encode('utf-8'))
            oprot.writeFieldEnd()
        if self.rateLimitDuration is not None:
            oprot.writeFieldBegin('rateLimitDuration', TType.I32, 3)
            oprot.writeI32(self.rateLimitDuration)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.errorCode is None:
            raise TProtocol.TProtocolException(message='Required field errorCode is unset!')
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __hash__(self):
        return hash((self.__class__, tuple(self.__dict__.items())))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class EDAMNotFoundException(TException):
    """
    This exception is thrown by EDAM procedures when a caller asks to perform
    an operation on an object that does not exist.  This may be thrown based on an invalid
    primary identifier (e.g. a bad GUID), or when the caller refers to an object
    by another unique identifier (e.g. a User's email address).

    identifier:  A description of the object that was not found on the server.
      For example, "Note.notebookGuid" when a caller attempts to create a note in a
      notebook that does not exist in the user's account.

    key:  The value passed from the client in the identifier, which was not
      found. For example, the GUID that was not found.

    Attributes:
     - identifier
     - key
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'identifier', None, None,),  # 1
        (2, TType.STRING, 'key', None, None,),  # 2
    )

    def __init__(self, identifier=None, key=None, ):
        TException.__init__(self)
        self.identifier = identifier
        self.key = key

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans,
                                                                                        TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.identifier = iprot.readString().decode('utf-8')
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.key = iprot.readString().decode('utf-8')
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('EDAMNotFoundException')
        if self.identifier is not None:
            oprot.writeFieldBegin('identifier', TType.STRING, 1)
            oprot.writeString(self.identifier.encode('utf-8'))
            oprot.writeFieldEnd()
        if self.key is not None:
            oprot.writeFieldBegin('key', TType.STRING, 2)
            oprot.writeString(self.key.encode('utf-8'))
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __hash__(self):
        return hash((self.__class__, tuple(self.__dict__.items())))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
