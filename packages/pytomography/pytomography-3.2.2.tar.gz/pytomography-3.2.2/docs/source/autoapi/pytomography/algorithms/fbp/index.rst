:py:mod:`pytomography.algorithms.fbp`
=====================================

.. py:module:: pytomography.algorithms.fbp

.. autoapi-nested-parse::

   This module contains classes that implement filtered back projection reconstruction algorithms.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.algorithms.fbp.FilteredBackProjection




.. py:class:: FilteredBackProjection(projections, system_matrix, filter=RampFilter)

   Implementation of filtered back projection reconstruction :math:`\hat{f} = \frac{\pi}{N_{\text{proj}}} \mathcal{R}^{-1}\mathcal{F}^{-1}\Pi\mathcal{F} g` where :math:`N_{\text{proj}}` is the number of projections, :math:`\mathcal{R}` is the 3D radon transform, :math:`\mathcal{F}` is the 2D Fourier transform (applied to each projection seperately), and :math:`\Pi` is the filter applied in Fourier space, which is by default the ramp filter.

   :param projections: projection data :math:`g` to be reconstructed
   :type projections: torch.Tensor
   :param system_matrix: system matrix for the imaging system. In FBP, phenomena such as attenuation and PSF should not be implemented in the system matrix
   :type system_matrix: SystemMatrix
   :param filter: Additional Fourier space filter (applied after Ramp Filter) used during reconstruction.
   :type filter: Callable, optional

   .. py:method:: __call__(projections)

      Applies reconstruction

      :returns: Reconstructed object prediction
      :rtype: torch.tensor



