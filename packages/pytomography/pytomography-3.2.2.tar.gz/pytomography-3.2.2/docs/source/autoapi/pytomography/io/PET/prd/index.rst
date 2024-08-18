:py:mod:`pytomography.io.PET.prd`
=================================

.. py:module:: pytomography.io.PET.prd


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   _binary/index.rst
   _dtypes/index.rst
   _ndjson/index.rst
   binary/index.rst
   ndjson/index.rst
   protocols/index.rst
   types/index.rst
   yardl_types/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd.OutOfRangeEnum
   pytomography.io.PET.prd.DateTime
   pytomography.io.PET.prd.Time
   pytomography.io.PET.prd.UnionCase
   pytomography.io.PET.prd.CoincidenceEvent
   pytomography.io.PET.prd.Detector
   pytomography.io.PET.prd.ExamInformation
   pytomography.io.PET.prd.Header
   pytomography.io.PET.prd.Institution
   pytomography.io.PET.prd.ScannerInformation
   pytomography.io.PET.prd.Subject
   pytomography.io.PET.prd.TimeBlock
   pytomography.io.PET.prd.TimeFrameInformation
   pytomography.io.PET.prd.TimeInterval
   pytomography.io.PET.prd.PrdExperimentReaderBase
   pytomography.io.PET.prd.PrdExperimentWriterBase
   pytomography.io.PET.prd.BinaryPrdExperimentReader
   pytomography.io.PET.prd.BinaryPrdExperimentWriter
   pytomography.io.PET.prd.NDJsonPrdExperimentReader
   pytomography.io.PET.prd.NDJsonPrdExperimentWriter



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd._parse_version
   pytomography.io.PET.prd.structural_equal



Attributes
~~~~~~~~~~

.. autoapisummary::

   pytomography.io.PET.prd._MIN_NUMPY_VERSION
   pytomography.io.PET.prd.Int8
   pytomography.io.PET.prd.UInt8
   pytomography.io.PET.prd.Int16
   pytomography.io.PET.prd.UInt16
   pytomography.io.PET.prd.Int32
   pytomography.io.PET.prd.UInt32
   pytomography.io.PET.prd.Int64
   pytomography.io.PET.prd.UInt64
   pytomography.io.PET.prd.Size
   pytomography.io.PET.prd.Float32
   pytomography.io.PET.prd.Float64
   pytomography.io.PET.prd.ComplexFloat
   pytomography.io.PET.prd.ComplexDouble
   pytomography.io.PET.prd._T
   pytomography.io.PET.prd.get_dtype


.. py:data:: _MIN_NUMPY_VERSION
   :value: (1, 22, 0)

   

.. py:function:: _parse_version(version)


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



.. py:class:: CoincidenceEvent(*, detector_1_id = 0, detector_2_id = 0, tof_idx = 0, energy_1_idx = 0, energy_2_idx = 0)

   All information about a coincidence event specified as identifiers or indices (i.e. discretized).
   TODO: this might take up too much space, so some/all of these could be combined in a single index if necessary.

   .. py:attribute:: detector_1_id
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: detector_2_id
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: tof_idx
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: energy_1_idx
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: energy_2_idx
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: Detector(*, id = 0, x = 0.0, y = 0.0, z = 0.0)

   Detector ID and location. Units are in mm
   TODO: this is currently just a sample implementation with "point" detectors.
   We plan to have full shape information here.

   .. py:attribute:: id
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: x
      :type: pytomography.io.PET.prd.yardl_types.Float32

      

   .. py:attribute:: y
      :type: pytomography.io.PET.prd.yardl_types.Float32

      

   .. py:attribute:: z
      :type: pytomography.io.PET.prd.yardl_types.Float32

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: ExamInformation(*, subject = None, institution = None, protocol = None, start_of_acquisition = None)

   Items describing the exam (incomplete)

   .. py:attribute:: subject
      :type: Subject

      

   .. py:attribute:: institution
      :type: Institution

      

   .. py:attribute:: protocol
      :type: Optional[str]

      

   .. py:attribute:: start_of_acquisition
      :type: Optional[pytomography.io.PET.prd.yardl_types.DateTime]

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: Header(*, scanner = None, exam = None)

   .. py:attribute:: scanner
      :type: ScannerInformation

      

   .. py:attribute:: exam
      :type: Optional[ExamInformation]

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: Institution(*, name = '', address = '')

   .. py:attribute:: name
      :type: str

      

   .. py:attribute:: address
      :type: str

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: ScannerInformation(*, model_name = None, detectors = None, tof_bin_edges = None, tof_resolution = 0.0, energy_bin_edges = None, energy_resolution_at_511 = 0.0, listmode_time_block_duration = 0)

   .. py:attribute:: model_name
      :type: Optional[str]

      

   .. py:attribute:: detectors
      :type: list[Detector]

      

   .. py:attribute:: tof_bin_edges
      :type: numpy.typing.NDArray[numpy.float32]

      edge information for TOF bins in mm (given as from first to last edge, so there is one more edge than the number of bins)
      TODO: this currently assumes equal size for each TOF bin, but some scanners "stretch" TOF bins depending on length of LOR

   .. py:attribute:: tof_resolution
      :type: pytomography.io.PET.prd.yardl_types.Float32

      TOF resolution in mm

   .. py:attribute:: energy_bin_edges
      :type: numpy.typing.NDArray[numpy.float32]

      edge information for energy windows in keV (given as from first to last edge, so there is one more edge than the number of bins)

   .. py:attribute:: energy_resolution_at_511
      :type: pytomography.io.PET.prd.yardl_types.Float32

      FWHM of photopeak for incoming gamma of 511 keV, expressed as a ratio w.r.t. 511

   .. py:attribute:: listmode_time_block_duration
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      duration of each time block in ms

   .. py:method:: number_of_detectors()


   .. py:method:: number_of_tof_bins()


   .. py:method:: number_of_energy_bins()


   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: Subject(*, name = None, id = '')

   .. py:attribute:: name
      :type: Optional[str]

      

   .. py:attribute:: id
      :type: str

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: TimeBlock(*, id = 0, prompt_events = None, delayed_events = None)

   .. py:attribute:: id
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      number of the block. Multiply with listmodeTimeBlockDuration to get time since startOfAcquisition

   .. py:attribute:: prompt_events
      :type: list[CoincidenceEvent]

      list of prompts in this time block
      TODO might be better to use !array

   .. py:attribute:: delayed_events
      :type: Optional[list[CoincidenceEvent]]

      list of delayed coincidences in this time block

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: TimeFrameInformation(*, time_frames = None)

   A sequence of time intervals (could be consecutive)

   .. py:attribute:: time_frames
      :type: list[TimeInterval]

      

   .. py:method:: number_of_time_frames()


   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:class:: TimeInterval(*, start = 0, stop = 0)

   Time interval in milliseconds since start of acquisition

   .. py:attribute:: start
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:attribute:: stop
      :type: pytomography.io.PET.prd.yardl_types.UInt32

      

   .. py:method:: __eq__(other)

      Return self==value.


   .. py:method:: __str__()

      Return str(self).


   .. py:method:: __repr__()

      Return repr(self).



.. py:data:: get_dtype

   

.. py:class:: PrdExperimentReaderBase

   Bases: :py:obj:`abc.ABC`

   Abstract reader for the PrdExperiment protocol.

   .. py:attribute:: schema

      

   .. py:attribute:: T

      

   .. py:method:: __enter__()


   .. py:method:: __exit__(exc_type, exc, traceback)


   .. py:method:: close()
      :abstractmethod:


   .. py:method:: read_header()

      Ordinal 0


   .. py:method:: read_time_blocks()

      Ordinal 1


   .. py:method:: copy_to(writer)


   .. py:method:: _read_header()
      :abstractmethod:


   .. py:method:: _read_time_blocks()
      :abstractmethod:


   .. py:method:: _wrap_iterable(iterable, final_state)


   .. py:method:: _raise_unexpected_state(actual)


   .. py:method:: _state_to_method_name(state)



.. py:class:: PrdExperimentWriterBase

   Bases: :py:obj:`abc.ABC`

   Abstract writer for the PrdExperiment protocol.

   .. py:attribute:: schema
      :value: '{"protocol":{"name":"PrdExperiment","sequence":[{"name":"header","type":"Prd.Header"},{"name":"ti...'

      

   .. py:method:: __enter__()


   .. py:method:: __exit__(exc_type, exc, traceback)


   .. py:method:: write_header(value)

      Ordinal 0


   .. py:method:: write_time_blocks(value)

      Ordinal 1


   .. py:method:: _write_header(value)
      :abstractmethod:


   .. py:method:: _write_time_blocks(value)
      :abstractmethod:


   .. py:method:: close()
      :abstractmethod:


   .. py:method:: _end_stream()
      :abstractmethod:


   .. py:method:: _raise_unexpected_state(actual)


   .. py:method:: _state_to_method_name(state)



.. py:class:: BinaryPrdExperimentReader(stream)

   Bases: :py:obj:`pytomography.io.PET.prd._binary.BinaryProtocolReader`, :py:obj:`pytomography.io.PET.prd.protocols.PrdExperimentReaderBase`

   Binary writer for the PrdExperiment protocol.

   .. py:method:: _read_header()


   .. py:method:: _read_time_blocks()



.. py:class:: BinaryPrdExperimentWriter(stream)

   Bases: :py:obj:`pytomography.io.PET.prd._binary.BinaryProtocolWriter`, :py:obj:`pytomography.io.PET.prd.protocols.PrdExperimentWriterBase`

   Binary writer for the PrdExperiment protocol.

   .. py:method:: _write_header(value)


   .. py:method:: _write_time_blocks(value)



.. py:class:: NDJsonPrdExperimentReader(stream)

   Bases: :py:obj:`pytomography.io.PET.prd._ndjson.NDJsonProtocolReader`, :py:obj:`pytomography.io.PET.prd.protocols.PrdExperimentReaderBase`

   NDJson writer for the PrdExperiment protocol.

   .. py:method:: _read_header()


   .. py:method:: _read_time_blocks()



.. py:class:: NDJsonPrdExperimentWriter(stream)

   Bases: :py:obj:`pytomography.io.PET.prd._ndjson.NDJsonProtocolWriter`, :py:obj:`pytomography.io.PET.prd.protocols.PrdExperimentWriterBase`

   NDJson writer for the PrdExperiment protocol.

   .. py:method:: _write_header(value)


   .. py:method:: _write_time_blocks(value)



