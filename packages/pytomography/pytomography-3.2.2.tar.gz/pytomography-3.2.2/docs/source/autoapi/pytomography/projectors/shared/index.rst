:py:mod:`pytomography.projectors.shared`
========================================

.. py:module:: pytomography.projectors.shared


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   kem_system_matrix/index.rst
   motion_correction_system_matrix/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.projectors.shared.KEMSystemMatrix
   pytomography.projectors.shared.MotionSystemMatrix




.. py:class:: KEMSystemMatrix(system_matrix, kem_transform)

   Bases: :py:obj:`pytomography.projectors.system_matrix.SystemMatrix`

   Given a KEM transform :math:`K` and a system matrix :math:`H`, implements the transform :math:`HK` (and backward transform :math:`K^T H^T`)

   :param system_matrix: System matrix corresponding to a particular imaging system
   :type system_matrix: SystemMatrix
   :param kem_transform: Transform used to go from coefficient image to real image of predicted counts.
   :type kem_transform: KEMTransform

   .. py:method:: compute_normalization_factor(subset_idx = None)

      Function used to get normalization factor :math:`K^T H^T_m 1` corresponding to projection subset :math:`m`.

      :param subset_idx: Index of subset. If none, then considers all projections. Defaults to None.
      :type subset_idx: int | None, optional

      :returns: normalization factor :math:`K^T H^T_m 1`
      :rtype: torch.Tensor


   .. py:method:: forward(object, subset_idx=None)

      Forward transform :math:`HK`

      :param object: Object to be forward projected
      :type object: torch.tensor
      :param subset_idx: Only uses a subset of angles :math:`g_m` corresponding to the provided subset index :math:`m`. If None, then defaults to the full projections :math:`g`.
      :type subset_idx: int, optional

      :returns: Corresponding projections generated from forward projection
      :rtype: torch.tensor


   .. py:method:: backward(proj, subset_idx=None)

      Backward transform :math:`K^T H^T`

      :param proj: Projection data to be back projected
      :type proj: torch.tensor
      :param subset_idx: Only uses a subset of angles :math:`g_m` corresponding to the provided subset index :math:`m`. If None, then defaults to the full projections :math:`g`.
      :type subset_idx: int, optional
      :param return_norm_constant: Additionally returns :math:`K^T H^T 1` if true; defaults to False.
      :type return_norm_constant: bool, optional

      :returns: Corresponding object generated from back projection.
      :rtype: torch.tensor



.. py:class:: MotionSystemMatrix(system_matrices, motion_transforms)

   Bases: :py:obj:`pytomography.projectors.system_matrix.ExtendedSystemMatrix`

   Abstract class for a general system matrix :math:`H:\mathbb{U} \to \mathbb{V}` which takes in an object :math:`f \in \mathbb{U}` and maps it to corresponding projections :math:`g \in \mathbb{V}` that would be produced by the imaging system. A system matrix consists of sequences of object-to-object and proj-to-proj transforms that model various characteristics of the imaging system, such as attenuation and blurring. While the class implements the operator :math:`H:\mathbb{U} \to \mathbb{V}` through the ``forward`` method, it also implements :math:`H^T:\mathbb{V} \to \mathbb{U}` through the `backward` method, required during iterative reconstruction algorithms such as OSEM.

   :param obj2obj_transforms: Sequence of object mappings that occur before forward projection.
   :type obj2obj_transforms: Sequence[Transform]
   :param im2im_transforms: Sequence of proj mappings that occur after forward projection.
   :type im2im_transforms: Sequence[Transform]
   :param object_meta: Object metadata.
   :type object_meta: ObjectMeta
   :param proj_meta: Projection metadata.
   :type proj_meta: ProjMeta


