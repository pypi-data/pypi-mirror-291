:py:mod:`pytomography.transforms.SPECT`
=======================================

.. py:module:: pytomography.transforms.SPECT


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   attenuation/index.rst
   psf/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.transforms.SPECT.SPECTAttenuationTransform
   pytomography.transforms.SPECT.SPECTPSFTransform




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



.. py:class:: SPECTPSFTransform(psf_meta = None, psf_operator = None, assume_padded = True)

   Bases: :py:obj:`pytomography.transforms.Transform`

   obj2obj transform used to model the effects of PSF blurring in SPECT. The smoothing kernel used to apply PSF modeling uses a Gaussian kernel with width :math:`\sigma` dependent on the distance of the point to the detector; that information is specified in the ``SPECTPSFMeta`` parameter. There are a few potential arguments to initialize this transform (i) `psf_meta`, which contains relevant collimator information to obtain a Gaussian PSF model that works for low/medium energy SPECT (ii) `kernel_f`, an callable function that gives the kernel at any source-detector distance :math:`d`, or (iii) `psf_operator`, a network configured to automatically apply full PSF modeling to a given object :math:`f` at all source-detector distances. Only one of the arguments should be given.

   :param psf_meta: Metadata corresponding to the parameters of PSF blurring. In most cases (low/medium energy SPECT), this should be the only given argument.
   :type psf_meta: SPECTPSFMeta
   :param kernel_f: Function :math:`PSF(x,y,d)` that gives PSF at every source-detector distance :math:`d`. It should be able to take in 1D numpy arrays as its first two arguments, and a single argument for the final argument :math:`d`. The function should return a corresponding 2D PSF kernel.
   :type kernel_f: Callable
   :param psf_operator: Network that takes in an object :math:`f` and applies all necessary PSF correction to return a new object :math:`\tilde{f}` that is PSF corrected, such that subsequent summation along the x-axis accurately models the collimator detector response.
   :type psf_operator: Callable

   .. py:method:: _configure_gaussian_model()

      Internal function to configure Gaussian modeling. This is called when `psf_meta` is given in initialization



   .. py:method:: _configure_manual_net()

      Internal function to configure the PSF net. This is called when `psf_operator` is given in initialization



   .. py:method:: configure(object_meta, proj_meta)

      Function used to initalize the transform using corresponding object and projection metadata

      :param object_meta: Object metadata.
      :type object_meta: SPECTObjectMeta
      :param proj_meta: Projections metadata.
      :type proj_meta: SPECTProjMeta


   .. py:method:: _compute_kernel_size(radius, axis)

      Function used to compute the kernel size used for PSF blurring. In particular, uses the ``min_sigmas`` attribute of ``SPECTPSFMeta`` to determine what the kernel size should be such that the kernel encompasses at least ``min_sigmas`` at all points in the object.

      :returns: The corresponding kernel size used for PSF blurring.
      :rtype: int


   .. py:method:: _get_sigma(radius)

      Uses PSF Meta data information to get blurring :math:`\sigma` as a function of distance from detector.

      :param radius: The distance from the detector.
      :type radius: float

      :returns: An array of length Lx corresponding to blurring at each point along the 1st axis in object space
      :rtype: array


   .. py:method:: forward(object, ang_idx)

      Applies the PSF transform :math:`A:\mathbb{U} \to \mathbb{U}` for the situation where an object is being detector by a detector at the :math:`+x` axis.

      :param object_i: Tensor of size [Lx, Ly, Lz] being projected along its first axis
      :type object_i: torch.tensor
      :param ang_idx: The projection indices: used to find the corresponding angle in projection space corresponding to each projection angle in ``object_i``.
      :type ang_idx: int

      :returns: Tensor of size [Lx, Ly, Lz] such that projection of this tensor along the first axis corresponds to n PSF corrected projection.
      :rtype: torch.tensor


   .. py:method:: backward(object, ang_idx)

      Applies the transpose of the PSF transform :math:`A^T:\mathbb{U} \to \mathbb{U}` for the situation where an object is being detector by a detector at the :math:`+x` axis. Since the PSF transform is a symmetric matrix, its implemtation is the same as the ``forward`` method.

      :param object_i: Tensor of size [Lx, Ly, Lz] being projected along its first axis
      :type object_i: torch.tensor
      :param ang_idx: The projection index
      :type ang_idx: int

      :returns: Tensor of size [Lx, Ly, Lz] such that projection of this tensor along the first axis corresponds to n PSF corrected projection.
      :rtype: torch.tensor



