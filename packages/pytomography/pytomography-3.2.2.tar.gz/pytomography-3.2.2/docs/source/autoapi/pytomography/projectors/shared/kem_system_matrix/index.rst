:py:mod:`pytomography.projectors.shared.kem_system_matrix`
==========================================================

.. py:module:: pytomography.projectors.shared.kem_system_matrix


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.projectors.shared.kem_system_matrix.KEMSystemMatrix




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



