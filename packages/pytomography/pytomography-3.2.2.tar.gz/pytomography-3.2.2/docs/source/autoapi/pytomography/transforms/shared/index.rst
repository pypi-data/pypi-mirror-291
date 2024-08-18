:py:mod:`pytomography.transforms.shared`
========================================

.. py:module:: pytomography.transforms.shared


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   filters/index.rst
   kem/index.rst
   motion/index.rst
   spatial/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.transforms.shared.KEMTransform
   pytomography.transforms.shared.GaussianFilter
   pytomography.transforms.shared.RotationTransform
   pytomography.transforms.shared.DVFMotionTransform




.. py:class:: KEMTransform(support_objects, support_kernels=None, support_kernels_params=None, distance_kernel=None, distance_kernel_params=None, size = 5, top_N = None, kernel_on_gpu = False)

   Bases: :py:obj:`pytomography.transforms.Transform`

   Object to object transform used to take in a coefficient image :math:`\alpha` and return an image estimate :math:`f = K\alpha`. This transform implements the matrix :math:`K`.

   :param support_objects: Objects used for support when building each basis function. These may correspond to PET/CT/MRI images, for example.
   :type support_objects: Sequence[torch.tensor]
   :param support_kernels: A list of functions corresponding to the support kernel of each support object. If none, defaults to :math:`k(v_i, v_j; \sigma) = \exp\left(-\frac{(v_i-v_j)^2}{2\sigma^2} \right)` for each support object. Defaults to None.
   :type support_kernels: Sequence[Callable], optional
   :param support_kernels_params: A list of lists, where each sublist contains the additional parameters corresponding to each support kernel (parameters that follow the semi-colon in the expression above). As an example, if using the default configuration for ``support_kernels`` for two different support objects (say CT and PET), one could given ``support_kernel_params=[[40],[5]]`` If none then defaults to a list of `N*[[1]]` where `N` is the number of support objects. Defaults to None.
   :type support_kernels_params: Sequence[Sequence[float]], optional
   :param distance_kernel: Kernel used to weight based on voxel-voxel distance. If none, defaults to :math:`k(x_i, x_j; \sigma) = \exp\left(-\frac{(x_i-x_j)^2}{2\sigma^2} \right) Defaults to None.
   :type distance_kernel: Callable, optional
   :param distance_kernel_params: A list of parameters corresponding to additional parameters for the ``distance_kernel`` (i.e. the parameters that follow the semi-colon in the expression above). If none, then defaults to :math:`\sigma=1`. Defaults to None.
   :type distance_kernel_params: _type_, optional
   :param size: The size of each kernel. Defaults to 5.
   :type size: int, optional

   .. py:method:: compute_kernel()

      Computes the kernel required for the KEM transform and stores internally



   .. py:method:: configure(object_meta, proj_meta)

      Function used to initalize the transform using corresponding object and projection metadata

      :param object_meta: Object metadata.
      :type object_meta: SPECTObjectMeta
      :param proj_meta: Projections metadata.
      :type proj_meta: SPECTProjMeta


   .. py:method:: forward(object)

      Forward transform corresponding to :math:`K\alpha`

      :param object: Coefficient image :math:`\alpha`
      :type object: torch.Tensor

      :returns: Image :math:`K\alpha`
      :rtype: torch.tensor


   .. py:method:: backward(object)

      Backward transform corresponding to :math:`K^T\alpha`. Since the matrix is symmetric, the implementation is the same as forward.

      :param object: Coefficient image :math:`\alpha`
      :type object: torch.Tensor

      :returns: Image :math:`K^T\alpha`
      :rtype: torch.tensor



.. py:class:: GaussianFilter(FWHM, n_sigmas = 3)

   Bases: :py:obj:`pytomography.transforms.Transform`

   Applies a Gaussian smoothing filter to the reconstructed object with the specified full-width-half-max (FWHM)

   :param FWHM: Specifies the width of the gaussian
   :type FWHM: float
   :param n_sigmas: Number of sigmas to include before truncating the kernel.
   :type n_sigmas: float

   .. py:method:: configure(object_meta, proj_meta)

      Configures the transform to the object/proj metadata. This is done after creating the network so that it can be adjusted to the system matrix.

      :param object_meta: Object metadata.
      :type object_meta: ObjectMeta
      :param proj_meta: Projections metadata.
      :type proj_meta: ProjMeta


   .. py:method:: _get_kernels()

      Obtains required kernels for smoothing



   .. py:method:: __call__(object)

      Alternative way to call


   .. py:method:: forward(object)

      Applies the Gaussian smoothing

      :param object: Object to smooth
      :type object: torch.tensor

      :returns: Smoothed object
      :rtype: torch.tensor


   .. py:method:: backward(object, norm_constant=None)

      Applies Gaussian smoothing in back projection. Because the operation is symmetric, it is the same as the forward projection.

      :param object: Object to smooth
      :type object: torch.tensor
      :param norm_constant: Normalization constant used in iterative algorithms. Defaults to None.
      :type norm_constant: torch.tensor, optional

      :returns: Smoothed object
      :rtype: torch.tensor



.. py:class:: RotationTransform(mode = 'bilinear')

   Bases: :py:obj:`pytomography.transforms.Transform`

   obj2obj transform used to rotate an object to angle :math:`\beta` in the DICOM reference frame. (Note that an angle of )

   :param mode: Interpolation mode used in the rotation.
   :type mode: str

   .. py:method:: forward(object, angles)

      Rotates an object to angle :math:`\beta` in the DICOM reference frame. Note that the scanner angle :math:`\beta` is related to :math:`\phi` (azimuthal angle) by :math:`\phi = 3\pi/2 - \beta`.

      :param object: Tensor of size [Lx, Ly, Lz] being rotated.
      :type object: torch.tensor
      :param angles: Tensor of size 1 corresponding to the rotation angle.
      :type angles: torch.Tensor

      :returns: Tensor of size [Lx, Ly, Lz] which is rotated
      :rtype: torch.tensor


   .. py:method:: backward(object, angles)

      Forward projection :math:`A:\mathbb{U} \to \mathbb{U}` of attenuation correction.

      :param object: Tensor of size [Lx, Ly, Lz] being rotated.
      :type object: torch.tensor
      :param angles: Tensor of size 1 corresponding to the rotation angle.
      :type angles: torch.Tensor

      :returns: Tensor of size [Lx, Ly, Lz] which is rotated.
      :rtype: torch.tensor



.. py:class:: DVFMotionTransform(dvf_forward = None, dvf_backward = None)

   Bases: :py:obj:`pytomography.transforms.Transform`

   The parent class for all transforms used in reconstruction (obj2obj, im2im, obj2im). Subclasses must implement the ``__call__`` method.

   :param device: Pytorch device used for computation
   :type device: str

   .. py:method:: _get_vol_ratio(DVF)


   .. py:method:: _get_old_coordinates()

      Obtain meshgrid of coordinates corresponding to the object

      :returns: Tensor of coordinates corresponding to input object
      :rtype: torch.Tensor


   .. py:method:: _get_new_coordinates(old_coordinates, DVF)

      Obtain the new coordinates of each voxel based on the DVF.

      :param old_coordinates: Old coordinates of each voxel
      :type old_coordinates: torch.Tensor
      :param DVF: Deformation vector field.
      :type DVF: torch.Tensor

      :returns: _description_
      :rtype: _type_


   .. py:method:: _apply_dvf(DVF, vol_ratio, object_i)

      Applies the deformation vector field to the object

      :param DVF: Deformation vector field
      :type DVF: torch.Tensor
      :param object_i: Old object.
      :type object_i: torch.Tensor

      :returns: Deformed object.
      :rtype: torch.Tensor


   .. py:method:: forward(object_i)

      Forward transform of deformation vector field

      :param object_i: Original object.
      :type object_i: torch.Tensor

      :returns: Deformed object corresponding to forward transform.
      :rtype: torch.Tensor


   .. py:method:: backward(object_i)

      Backward transform of deformation vector field

      :param object_i: Original object.
      :type object_i: torch.Tensor

      :returns: Deformed object corresponding to backward transform.
      :rtype: torch.Tensor



