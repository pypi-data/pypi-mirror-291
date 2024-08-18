:py:mod:`pytomography.metadata.PET.petlm_metadata`
==================================================

.. py:module:: pytomography.metadata.PET.petlm_metadata


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.metadata.PET.petlm_metadata.PETLMProjMeta




.. py:class:: PETLMProjMeta(detector_ids, info = None, scanner_LUT = None, tof_meta = None, weights = None, detector_ids_sensitivity = None, weights_sensitivity = None)

   Metadata required for PET listmode modeling. PET listmode projection actually requires two different projectors: the system matrix that projects to all detected crystal pair LORs (which is denoted as :math:`H`) and the system matrix that projects to all valid LORs (denoted as :math:`\tilde{H}`). The system matrix :math:`H` is used for forward/back projection in reconstruction algorithms, while :math:`\tilde{H}` is used for computing the normalization image :math:`\tilde{H}^T 1`.
   :param detector_ids: :math:`N \times 2` (non-TOF) or :math:`N \times 3` (TOF) tensor that provides detector ID pairs (and TOF bin) for coincidence events. This information is used to construct :math:`H`.
   :type detector_ids: torch.Tensor
   :param info: Dictionary containing all relevant information about the scanner. If ``scanner_LUT`` is not provided, then info is used to create the ``scanner_LUT``. At least one of ``info`` or ``scanner_LUT`` should be provided as input arguments.
   :type info: dict, optional
   :param scanner_LUT: scanner lookup table that provides spatial coordinates for all detector ID pairs. If ``info`` is not provided, then ``scanner_LUT`` must be provided.
   :type scanner_LUT: torch.Tensor, optional
   :param tof_meta: PET time-of-flight metadata used to modify :math:`H` for time of flight projection. If None, then time of flight is not used. Defaults to None.
   :type tof_meta: PETTOFMeta | None, optional
   :param weights: weights used to scale projections after forward projection and before back projection; these modify the system matrix :math:`H`. While such weights can be used to apply attenuation/normalization correction, they aren't required in the absence of randoms/scatter; these correction need only be performed using ``weights_sensitivity``. If provided, these weights must have the number of elements as the first dimension of ``detector_ids``. If none, then no scaling is done. Defaults to None.
   :type weights: torch.tensor | None, optional
   :param detector_ids_sensitivity: valid detector ids used to generate the sensitivity image :math:`\tilde{H}^T 1`. As such, these are used to construct :math:`\tilde{H}`. If None, then assumes all detector ids (specified by ``scanner_LUT``) are valid. Defaults to None.
   :type detector_ids_sensitivity: torch.tensor | None, optional
   :param weights_sensitivity: weights used for scaling projections in the computation of the sensitivity image, if the weights are given as :math:`w` then the sensitivty image becomes :math:`\tilde{H}^T w`; these modify the system matrix :math:`\tilde{H}`. These weights are used for attenuation/normalization correction. If ``detector_ids_sensitivity`` is provided, then ``weights_sensitivity`` should have the same shape. If ``detector_ids_sensitivity`` is not provided, then ``weights_sensitivity`` should be the same length as all possible combinations of detectors in the ``scanner_LUT``. If None, then no scaling is performed. Defaults to None.
   :type weights_sensitivity: torch.tensor | None, optional


