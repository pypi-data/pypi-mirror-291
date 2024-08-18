:py:mod:`pytomography.transforms.SPECT.attenuation`
===================================================

.. py:module:: pytomography.transforms.SPECT.attenuation


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.transforms.SPECT.attenuation.SPECTAttenuationTransform



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.transforms.SPECT.attenuation.get_prob_of_detection_matrix



.. py:function:: get_prob_of_detection_matrix(attenuation_map, dx)

   Converts an attenuation map of :math:`\text{cm}^{-1}` to a probability of photon detection matrix (scanner at +x). Note that this requires the attenuation map to be at the energy of photons being emitted.

   :param attenuation_map: Tensor of size [Lx, Ly, Lz] corresponding to the attenuation coefficient in :math:`{\text{cm}^{-1}}
   :type attenuation_map: torch.tensor
   :param dx: Axial plane pixel spacing.
   :type dx: float

   :returns: Tensor of size [Lx, Ly, Lz] corresponding to probability of photon being detected at detector at +x axis.
   :rtype: torch.tensor


.. py:class:: SPECTAttenuationTransform(attenuation_map = None, filepath = None, mode = 'constant', assume_padded = True, HU2mu_technique = 'from_table')

   Bases: :py:obj:`pytomography.transforms.Transform`

   obj2obj transform used to model the effects of attenuation in SPECT. This transform accepts either an ``attenuation_map`` (which must be aligned with the SPECT projection data) or a ``filepath`` consisting of folder containing CT DICOM files all pertaining to the same scan

   :param attenuation_map: Tensor of size [Lx, Ly, Lz] corresponding to the attenuation coefficient in :math:`{\text{cm}^{-1}}` at the photon energy corresponding to the particular scan
   :type attenuation_map: torch.tensor
   :param filepath: Folder location of CT scan; all .dcm files must correspond to different slices of the same scan.
   :type filepath: Sequence[str]
   :param mode: Mode used for extrapolation of CT beyond edges when aligning DICOM SPECT/CT data. Defaults to `'constant'`, which means the image is padded with zeros.
   :type mode: str
   :param assume_padded: Assumes objects and projections fed into forward and backward methods are padded, as they will be in reconstruction algorithms
   :type assume_padded: bool
   :param HU2mu_technique: Technique to convert HU to attenuation coefficients. The default, 'from_table', uses a table of coefficients for bilinear curves obtained for a variety of common radionuclides. The technique 'from_cortical_bone_fit' looks for a cortical bone peak in the scan and uses that to obtain the bilinear coefficients. For phantom scans where the attenuation coefficient is always significantly less than bone, the corticol bone technique will still work, since the first part of the bilinear curve (in the air to water range) does not depend on the cortical bone fit. Alternatively, one can provide an arbitrary function here which takes in a 3D scan with units of HU and converts to mu.
   :type HU2mu_technique: str

   .. py:method:: configure(object_meta, proj_meta)

      Function used to initalize the transform using corresponding object and projection metadata

      :param object_meta: Object metadata.
      :type object_meta: SPECTObjectMeta
      :param proj_meta: Projection metadata.
      :type proj_meta: SPECTProjMeta


   .. py:method:: forward(object_i, ang_idx)

      Forward projection :math:`A:\mathbb{U} \to \mathbb{U}` of attenuation correction.

      :param object_i: Tensor of size [Lx, Ly, Lz] being projected along ``axis=0``.
      :type object_i: torch.tensor
      :param ang_idx: The projection indices: used to find the corresponding angle in projection space corresponding to each projection angle in ``object_i``.
      :type ang_idx: torch.Tensor

      :returns: Tensor of size [Lx, Ly, Lz] such that projection of this tensor along the first axis corresponds to an attenuation corrected projection.
      :rtype: torch.tensor


   .. py:method:: backward(object_i, ang_idx)

      Back projection :math:`A^T:\mathbb{U} \to \mathbb{U}` of attenuation correction. Since the matrix is diagonal, the implementation is the same as forward projection. The only difference is the optional normalization parameter.

      :param object_i: Tensor of size [Lx, Ly, Lz] being projected along ``axis=0``.
      :type object_i: torch.tensor
      :param ang_idx: The projection indices: used to find the corresponding angle in projection space corresponding to each projection angle in ``object_i``.
      :type ang_idx: torch.Tensor
      :param norm_constant: A tensor used to normalize the output during back projection. Defaults to None.
      :type norm_constant: torch.tensor, optional

      :returns: Tensor of size [Lx, Ly, Lz] such that projection of this tensor along the first axis corresponds to an attenuation corrected projection.
      :rtype: torch.tensor


   .. py:method:: compute_average_prob_matrix()



