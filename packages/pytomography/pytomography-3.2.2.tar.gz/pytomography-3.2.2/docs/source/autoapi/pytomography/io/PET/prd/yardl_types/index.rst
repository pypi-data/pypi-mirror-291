:py:mod:`pytomography.io.PET.prd.yardl_types`
=============================================

.. py:module:: pytomography.io.PET.prd.yardl_types


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd.yardl_types.OutOfRangeEnum
   pytomography.io.PET.prd.yardl_types.DateTime
   pytomography.io.PET.prd.yardl_types.Time
   pytomography.io.PET.prd.yardl_types.UnionCase



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd.yardl_types.structural_equal



Attributes
~~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd.yardl_types.Int8
   pytomography.io.PET.prd.yardl_types.UInt8
   pytomography.io.PET.prd.yardl_types.Int16
   pytomography.io.PET.prd.yardl_types.UInt16
   pytomography.io.PET.prd.yardl_types.Int32
   pytomography.io.PET.prd.yardl_types.UInt32
   pytomography.io.PET.prd.yardl_types.Int64
   pytomography.io.PET.prd.yardl_types.UInt64
   pytomography.io.PET.prd.yardl_types.Size
   pytomography.io.PET.prd.yardl_types.Float32
   pytomography.io.PET.prd.yardl_types.Float64
   pytomography.io.PET.prd.yardl_types.ComplexFloat
   pytomography.io.PET.prd.yardl_types.ComplexDouble
   pytomography.io.PET.prd.yardl_types._T


.. py:exception:: ProtocolError

   Bases: :py:obj:`Exception`

   Raised when the contract of a protocol is not respected.


.. py:class:: OutOfRangeEnum(*args, **kwds)

   Bases: :py:obj:`enum.Enum`

   Enum that allows values outside of the its defined values.

   .. py:method:: _missing_(value)
      :classmethod:


   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __hash__()

      Return hash(self).


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: DateTime(nanoseconds_from_epoch = 0)

   A basic datetime with nanosecond precision, always in UTC.

   .. py:property:: numpy_value
      :type: numpy.datetime64


   .. py:method:: to_datetime()


   .. py:method:: from_components(year, month, day, hour = 0, minute = 0, second = 0, nanosecond = 0)
      :staticmethod:


   .. py:method:: from_datetime(dt)
      :staticmethod:


   .. py:method:: parse(s)
      :staticmethod:


   .. py:method:: now()
      :staticmethod:


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).


   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __hash__()

      Return hash(self).



.. py:class:: Time(nanoseconds_since_midnight = 0)

   A basic time of day with nanosecond precision. It is not timezone-aware and is meant
   to represent a wall clock time.

   .. py:property:: numpy_value
      :type: numpy.timedelta64


   .. py:attribute:: _NANOSECONDS_PER_DAY

      

   .. py:method:: from_components(hour, minute, second = 0, nanosecond = 0)
      :staticmethod:


   .. py:method:: from_time(t)
      :staticmethod:


   .. py:method:: parse(s)
      :staticmethod:


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).


   .. py:method:: __eq__(other)

      Return self==value.



.. py:data:: Int8

   

.. py:data:: UInt8

   

.. py:data:: Int16

   

.. py:data:: UInt16

   

.. py:data:: Int32

   

.. py:data:: UInt32

   

.. py:data:: Int64

   

.. py:data:: UInt64

   

.. py:data:: Size

   

.. py:data:: Float32

   

.. py:data:: Float64

   

.. py:data:: ComplexFloat

   

.. py:data:: ComplexDouble

   

.. py:function:: structural_equal(a, b)


.. py:data:: _T

   

.. py:class:: UnionCase(value)

   Bases: :py:obj:`abc.ABC`, :py:obj:`Generic`\ [\ :py:obj:`_T`\ ]

   Helper class that provides a standard way to create an ABC using
   inheritance.

   .. py:attribute:: index
      :type: int

      

   .. py:attribute:: tag
      :type: str

      

   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).


   .. py:method:: __eq__(other)

      Return self==value.



