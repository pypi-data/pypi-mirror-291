:py:mod:`pytomography.transforms.SPECT.psf`
===========================================

.. py:module:: pytomography.transforms.SPECT.psf


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.transforms.SPECT.psf.GaussianBlurNet
   pytomography.transforms.SPECT.psf.PSF2D
   pytomography.transforms.SPECT.psf.SPECTPSFTransform



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.transforms.SPECT.psf.get_1D_PSF_layer



.. py:class:: GaussianBlurNet(layer_r, layer_z = None)

   Bases: :py:obj:`torch.nn.Module`

   Network used to apply Gaussian blurring to each plane parallel to the detector head. The typical network used for low/medium energy SPECT PSF modeling.

   :param layer_r: Kernel used for blurring in radial direction
   :type layer_r: nn.Conv1d
   :param layer_z: Kernel used for blurring in sup/inf direction.
   :type layer_z: nn.Conv1d | None

   .. py:method:: forward(input)

      Applies PSF blurring to `input`. Each X-plane gets a different blurring kernel applied, depending on detector distance.

      :param input: Object to apply Gaussian blurring to
      :type input: torch.tensor

      :returns: Blurred object, adjusted such that subsequent summation along the x-axis models the CDR
      :rtype: torch.tensor



.. py:class:: PSF2D(psf_operator, distances, kernel_size, dr)

   .. py:method:: __call__(input)



.. py:function:: get_1D_PSF_layer(sigmas, kernel_size)

   Creates a 1D convolutional layer that is used for PSF modeling.

   :param sigmas: Array of length Lx corresponding to blurring (sigma of Gaussian) as a function of distance from scanner
   :type sigmas: array
   :param kernel_size: Size of the kernel used in each layer. Needs to be large enough to cover most of Gaussian
   :type kernel_size: int

   :returns: Convolutional neural network layer used to apply blurring to objects of shape [Lx, L1, L2] where Lx is treated as a batch size, L1 as the channel (or group index) and L2 is the axis being blurred over
   :rtype: torch.nn.Conv2d


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



