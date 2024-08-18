:py:mod:`pytomography.io.PET.prd._binary`
=========================================

.. py:module:: pytomography.io.PET.prd._binary


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd._binary.BinaryProtocolWriter
   pytomography.io.PET.prd._binary.BinaryProtocolReader
   pytomography.io.PET.prd._binary.CodedOutputStream
   pytomography.io.PET.prd._binary.CodedInputStream
   pytomography.io.PET.prd._binary.TypeSerializer
   pytomography.io.PET.prd._binary.StructSerializer
   pytomography.io.PET.prd._binary.BoolSerializer
   pytomography.io.PET.prd._binary.Int8Serializer
   pytomography.io.PET.prd._binary.UInt8Serializer
   pytomography.io.PET.prd._binary.Int16Serializer
   pytomography.io.PET.prd._binary.UInt16Serializer
   pytomography.io.PET.prd._binary.Int32Serializer
   pytomography.io.PET.prd._binary.UInt32Serializer
   pytomography.io.PET.prd._binary.Int64Serializer
   pytomography.io.PET.prd._binary.UInt64Serializer
   pytomography.io.PET.prd._binary.SizeSerializer
   pytomography.io.PET.prd._binary.Float32Serializer
   pytomography.io.PET.prd._binary.Float64Serializer
   pytomography.io.PET.prd._binary.Complex32Serializer
   pytomography.io.PET.prd._binary.Complex64Serializer
   pytomography.io.PET.prd._binary.StringSerializer
   pytomography.io.PET.prd._binary.DateSerializer
   pytomography.io.PET.prd._binary.TimeSerializer
   pytomography.io.PET.prd._binary.DateTimeSerializer
   pytomography.io.PET.prd._binary.NoneSerializer
   pytomography.io.PET.prd._binary.EnumSerializer
   pytomography.io.PET.prd._binary.OptionalSerializer
   pytomography.io.PET.prd._binary.UnionCaseProtocol
   pytomography.io.PET.prd._binary.UnionSerializer
   pytomography.io.PET.prd._binary.StreamSerializer
   pytomography.io.PET.prd._binary.FixedVectorSerializer
   pytomography.io.PET.prd._binary.VectorSerializer
   pytomography.io.PET.prd._binary.MapSerializer
   pytomography.io.PET.prd._binary.NDArraySerializerBase
   pytomography.io.PET.prd._binary.DynamicNDArraySerializer
   pytomography.io.PET.prd._binary.NDArraySerializer
   pytomography.io.PET.prd._binary.FixedNDArraySerializer
   pytomography.io.PET.prd._binary.RecordSerializer



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd._binary.write_fixed_int32
   pytomography.io.PET.prd._binary.read_fixed_int32



Attributes
~~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd._binary.MAGIC_BYTES
   pytomography.io.PET.prd._binary.CURRENT_BINARY_FORMAT_VERSION
   pytomography.io.PET.prd._binary.INT8_MIN
   pytomography.io.PET.prd._binary.INT8_MAX
   pytomography.io.PET.prd._binary.UINT8_MAX
   pytomography.io.PET.prd._binary.INT16_MIN
   pytomography.io.PET.prd._binary.INT16_MAX
   pytomography.io.PET.prd._binary.UINT16_MAX
   pytomography.io.PET.prd._binary.INT32_MIN
   pytomography.io.PET.prd._binary.INT32_MAX
   pytomography.io.PET.prd._binary.UINT32_MAX
   pytomography.io.PET.prd._binary.INT64_MIN
   pytomography.io.PET.prd._binary.INT64_MAX
   pytomography.io.PET.prd._binary.UINT64_MAX
   pytomography.io.PET.prd._binary.T
   pytomography.io.PET.prd._binary.T_NP
   pytomography.io.PET.prd._binary.bool_serializer
   pytomography.io.PET.prd._binary.int8_serializer
   pytomography.io.PET.prd._binary.uint8_serializer
   pytomography.io.PET.prd._binary.int16_serializer
   pytomography.io.PET.prd._binary.uint16_serializer
   pytomography.io.PET.prd._binary.int32_serializer
   pytomography.io.PET.prd._binary.uint32_serializer
   pytomography.io.PET.prd._binary.int64_serializer
   pytomography.io.PET.prd._binary.uint64_serializer
   pytomography.io.PET.prd._binary.size_serializer
   pytomography.io.PET.prd._binary.float32_serializer
   pytomography.io.PET.prd._binary.float64_serializer
   pytomography.io.PET.prd._binary.complexfloat32_serializer
   pytomography.io.PET.prd._binary.complexfloat64_serializer
   pytomography.io.PET.prd._binary.string_serializer
   pytomography.io.PET.prd._binary.EPOCH_ORDINAL_DAYS
   pytomography.io.PET.prd._binary.DATETIME_DAYS_DTYPE
   pytomography.io.PET.prd._binary.date_serializer
   pytomography.io.PET.prd._binary.TIMEDELTA_NANOSECONDS_DTYPE
   pytomography.io.PET.prd._binary.time_serializer
   pytomography.io.PET.prd._binary.DATETIME_NANOSECONDS_DTYPE
   pytomography.io.PET.prd._binary.EPOCH_DATETIME
   pytomography.io.PET.prd._binary.datetime_serializer
   pytomography.io.PET.prd._binary.none_serializer
   pytomography.io.PET.prd._binary.TEnum
   pytomography.io.PET.prd._binary.TKey
   pytomography.io.PET.prd._binary.TKey_NP
   pytomography.io.PET.prd._binary.TValue
   pytomography.io.PET.prd._binary.TValue_NP
   pytomography.io.PET.prd._binary.int32_struct


.. py:data:: MAGIC_BYTES
   :type: bytes
   :value: b'yardl'

   

.. py:data:: CURRENT_BINARY_FORMAT_VERSION
   :type: int
   :value: 1

   

.. py:data:: INT8_MIN
   :type: int

   

.. py:data:: INT8_MAX
   :type: int

   

.. py:data:: UINT8_MAX
   :type: int

   

.. py:data:: INT16_MIN
   :type: int

   

.. py:data:: INT16_MAX
   :type: int

   

.. py:data:: UINT16_MAX
   :type: int

   

.. py:data:: INT32_MIN
   :type: int

   

.. py:data:: INT32_MAX
   :type: int

   

.. py:data:: UINT32_MAX
   :type: int

   

.. py:data:: INT64_MIN
   :type: int

   

.. py:data:: INT64_MAX
   :type: int

   

.. py:data:: UINT64_MAX
   :type: int

   

.. py:class:: BinaryProtocolWriter(stream, schema)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.ABC`

   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:method:: close()


   .. py:method:: _end_stream()



.. py:class:: BinaryProtocolReader(stream, expected_schema)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.ABC`

   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:method:: close()



.. py:class:: CodedOutputStream(stream, *, buffer_size = 65536)

   .. py:method:: close()


   .. py:method:: ensure_capacity(size)


   .. py:method:: flush()


   .. py:method:: write(formatter, *args)


   .. py:method:: write_bytes(data)


   .. py:method:: write_bytes_directly(data)


   .. py:method:: write_byte_no_check(value)


   .. py:method:: write_unsigned_varint(value)


   .. py:method:: zigzag_encode(value)


   .. py:method:: write_signed_varint(value)



.. py:class:: CodedInputStream(stream, *, buffer_size = 65536)

   .. py:method:: close()


   .. py:method:: read(formatter)


   .. py:method:: read_byte()


   .. py:method:: read_unsigned_varint()


   .. py:method:: zigzag_decode(value)


   .. py:method:: read_signed_varint()


   .. py:method:: read_view(count)


   .. py:method:: read_bytearray(count)


   .. py:method:: _fill_buffer(min_count = 0)



.. py:data:: T

   

.. py:data:: T_NP

   

.. py:class:: TypeSerializer(dtype)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`pytomography.io.PET.prd.yardl_types.ABC`

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: overall_dtype()


   .. py:method:: struct_format_str()


   .. py:method:: write(stream, value)
      :abstractmethod:


   .. py:method:: write_numpy(stream, value)
      :abstractmethod:


   .. py:method:: read(stream)
      :abstractmethod:


   .. py:method:: read_numpy(stream)
      :abstractmethod:


   .. py:method:: is_trivially_serializable()



.. py:class:: StructSerializer(numpy_type, format_string)

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: struct_format_str()



.. py:class:: BoolSerializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`bool`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.bool_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: bool_serializer

   

.. py:class:: Int8Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Int8`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.int8`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: read(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: int8_serializer

   

.. py:class:: UInt8Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.UInt8`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.uint8`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: read(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: uint8_serializer

   

.. py:class:: Int16Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Int16`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.int16`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: int16_serializer

   

.. py:class:: UInt16Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.UInt16`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.uint16`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: uint16_serializer

   

.. py:class:: Int32Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Int32`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.int32`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: int32_serializer

   

.. py:class:: UInt32Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.UInt32`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.uint32`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: uint32_serializer

   

.. py:class:: Int64Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Int64`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.int64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: int64_serializer

   

.. py:class:: UInt64Serializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.UInt64`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.uint64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: uint64_serializer

   

.. py:class:: SizeSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Size`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.uint64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: size_serializer

   

.. py:class:: Float32Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Float32`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.float32`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: read(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: float32_serializer

   

.. py:class:: Float64Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Float64`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.float64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: read(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: float64_serializer

   

.. py:class:: Complex32Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.ComplexFloat`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.complex64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: complexfloat32_serializer

   

.. py:class:: Complex64Serializer

   Bases: :py:obj:`StructSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.ComplexDouble`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.complex128`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: is_trivially_serializable()



.. py:data:: complexfloat64_serializer

   

.. py:class:: StringSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`str`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: string_serializer

   

.. py:data:: EPOCH_ORDINAL_DAYS

   

.. py:data:: DATETIME_DAYS_DTYPE

   

.. py:class:: DateSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.datetime.date`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.datetime64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: date_serializer

   

.. py:data:: TIMEDELTA_NANOSECONDS_DTYPE

   

.. py:class:: TimeSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.Time`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.timedelta64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: time_serializer

   

.. py:data:: DATETIME_NANOSECONDS_DTYPE

   

.. py:data:: EPOCH_DATETIME

   

.. py:class:: DateTimeSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`pytomography.io.PET.prd.yardl_types.DateTime`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.datetime64`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: datetime_serializer

   

.. py:class:: NoneSerializer

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`None`\ , :py:obj:`Any`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: none_serializer

   

.. py:data:: TEnum

   

.. py:class:: EnumSerializer(integer_serializer, enum_type)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`TEnum`\ , :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`TEnum`\ , :py:obj:`T_NP`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: is_trivially_serializable()



.. py:class:: OptionalSerializer(element_serializer)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`Optional`\ [\ :py:obj:`T`\ ]\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.void`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: is_trivially_serializable()



.. py:class:: UnionCaseProtocol

   Bases: :py:obj:`Protocol`

   Base class for protocol classes.

   Protocol classes are defined as::

       class Proto(Protocol):
           def meth(self) -> int:
               ...

   Such classes are primarily used with static type checkers that recognize
   structural subtyping (static duck-typing).

   For example::

       class C:
           def meth(self) -> int:
               return 0

       def func(x: Proto) -> int:
           return x.meth()

       func(C())  # Passes static type check

   See PEP 544 for details. Protocol classes decorated with
   @typing.runtime_checkable act as simple-minded runtime protocols that check
   only the presence of given attributes, ignoring their type signatures.
   Protocol classes can be generic, they are defined as::

       class GenProto(Protocol[T]):
           def meth(self) -> T:
               ...

   .. py:attribute:: index
      :type: int

      

   .. py:attribute:: value
      :type: Any

      


.. py:class:: UnionSerializer(union_type, cases)

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`T`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:class:: StreamSerializer(element_serializer)

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`Iterable`\ [\ :py:obj:`T`\ ]\ , :py:obj:`Any`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)
      :abstractmethod:


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)
      :abstractmethod:



.. py:class:: FixedVectorSerializer(element_serializer, length)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`list`\ [\ :py:obj:`T`\ ]\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)
      :abstractmethod:


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)
      :abstractmethod:


   .. py:method:: is_trivially_serializable()



.. py:class:: VectorSerializer(element_serializer)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`list`\ [\ :py:obj:`T`\ ]\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: TKey

   

.. py:data:: TKey_NP

   

.. py:data:: TValue

   

.. py:data:: TValue_NP

   

.. py:class:: MapSerializer(key_serializer, value_serializer)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`TKey`\ , :py:obj:`TKey_NP`\ , :py:obj:`TValue`\ , :py:obj:`TValue_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`dict`\ [\ :py:obj:`TKey`\ , :py:obj:`TValue`\ ]\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:class:: NDArraySerializerBase(overall_dtype, element_serializer, dtype)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`TypeSerializer`\ [\ :py:obj:`numpy.typing.NDArray`\ [\ :py:obj:`Any`\ ]\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.object_`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: _get_dtype_and_subarray_shape(dtype)
      :staticmethod:


   .. py:method:: _write_data(stream, value)


   .. py:method:: _read_data(stream, shape)


   .. py:method:: _is_current_array_trivially_serializable(value)



.. py:class:: DynamicNDArraySerializer(element_serializer)

   Bases: :py:obj:`NDArraySerializerBase`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:class:: NDArraySerializer(element_serializer, ndims)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`NDArraySerializerBase`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)



.. py:class:: FixedNDArraySerializer(element_serializer, shape)

   Bases: :py:obj:`pytomography.io.PET.prd.yardl_types.Generic`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ], :py:obj:`NDArraySerializerBase`\ [\ :py:obj:`T`\ , :py:obj:`T_NP`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: write(stream, value)


   .. py:method:: write_numpy(stream, value)


   .. py:method:: read(stream)


   .. py:method:: read_numpy(stream)


   .. py:method:: is_trivially_serializable()



.. py:class:: RecordSerializer(field_serializers)

   Bases: :py:obj:`TypeSerializer`\ [\ :py:obj:`T`\ , :py:obj:`pytomography.io.PET.prd.yardl_types.np.void`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:method:: is_trivially_serializable()


   .. py:method:: _write(stream, *values)


   .. py:method:: _read(stream)


   .. py:method:: read_numpy(stream)



.. py:data:: int32_struct

   

.. py:function:: write_fixed_int32(stream, value)


.. py:function:: read_fixed_int32(stream)


