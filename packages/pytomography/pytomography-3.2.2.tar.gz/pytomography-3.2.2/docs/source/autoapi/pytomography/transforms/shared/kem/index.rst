:py:mod:`pytomography.transforms.shared.kem`
============================================

.. py:module:: pytomography.transforms.shared.kem


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.transforms.shared.kem.KEMTransform




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



