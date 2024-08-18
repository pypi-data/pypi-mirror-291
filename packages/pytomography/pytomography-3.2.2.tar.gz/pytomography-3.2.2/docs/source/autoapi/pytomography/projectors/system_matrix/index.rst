:py:mod:`pytomography.projectors.system_matrix`
===============================================

.. py:module:: pytomography.projectors.system_matrix


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.projectors.system_matrix.SystemMatrix
   pytomography.projectors.system_matrix.ExtendedSystemMatrix




.. py:class:: SystemMatrix(object_meta, proj_meta, obj2obj_transforms = [], proj2proj_transforms = [])

   Abstract class for a general system matrix :math:`H:\mathbb{U} \to \mathbb{V}` which takes in an object :math:`f \in \mathbb{U}` and maps it to corresponding projections :math:`g \in \mathbb{V}` that would be produced by the imaging system. A system matrix consists of sequences of object-to-object and proj-to-proj transforms that model various characteristics of the imaging system, such as attenuation and blurring. While the class implements the operator :math:`H:\mathbb{U} \to \mathbb{V}` through the ``forward`` method, it also implements :math:`H^T:\mathbb{V} \to \mathbb{U}` through the `backward` method, required during iterative reconstruction algorithms such as OSEM.

   :param obj2obj_transforms: Sequence of object mappings that occur before forward projection.
   :type obj2obj_transforms: Sequence[Transform]
   :param im2im_transforms: Sequence of proj mappings that occur after forward projection.
   :type im2im_transforms: Sequence[Transform]
   :param object_meta: Object metadata.
   :type object_meta: ObjectMeta
   :param proj_meta: Projection metadata.
   :type proj_meta: ProjMeta

   .. py:method:: initialize_transforms()

      Initializes all transforms used to build the system matrix



   .. py:method:: _get_object_initial(device=None)

      Returns an initial object estimate used in reconstruction algorithms. By default, this is a tensor of ones with the same shape as the object metadata.

      :returns: Initial object used in image reconstruction algorithms.
      :rtype: torch.Tensor


   .. py:method:: _get_prior_FOV_scale()

      Sets scaling for the prior within the FOV.

      :returns: Prior scaling
      :rtype: torch.Tensor


   .. py:method:: forward(object, **kwargs)
      :abstractmethod:

      Implements forward projection :math:`Hf` on an object :math:`f`.

      :param object: The object to be forward projected
      :type object: torch.tensor[batch_size, Lx, Ly, Lz]
      :param angle_subset: Only uses a subset of angles (i.e. only certain values of :math:`j` in formula above) when back projecting. Useful for ordered-subset reconstructions. Defaults to None, which assumes all angles are used.
      :type angle_subset: list, optional

      :returns: Forward projected proj where Ltheta is specified by `self.proj_meta` and `angle_subset`.
      :rtype: torch.tensor[batch_size, Ltheta, Lx, Lz]


   .. py:method:: backward(proj, angle_subset = None, return_norm_constant = False)
      :abstractmethod:

      Implements back projection :math:`H^T g` on a set of projections :math:`g`.

      :param proj: proj which is to be back projected
      :type proj: torch.Tensor
      :param angle_subset: Only uses a subset of angles (i.e. only certain values of :math:`j` in formula above) when back projecting. Useful for ordered-subset reconstructions. Defaults to None, which assumes all angles are used.
      :type angle_subset: list, optional
      :param return_norm_constant: Whether or not to return :math:`1/\sum_j H_{ij}` along with back projection. Defaults to 'False'.
      :type return_norm_constant: bool

      :returns: the object obtained from back projection.
      :rtype: torch.tensor[batch_size, Lr, Lr, Lz]


   .. py:method:: get_subset_splits(n_subsets)
      :abstractmethod:

      Returns a list of subsets corresponding to a partition of the projection data used in a reconstruction algorithm.

      :param n_subsets: number of subsets used in OSEM
      :type n_subsets: int

      :returns: list of index arrays for each subset
      :rtype: list



.. py:class:: ExtendedSystemMatrix(system_matrices, obj2obj_transforms = None, proj2proj_transforms = None)

   Bases: :py:obj:`SystemMatrix`

   Abstract class for a general system matrix :math:`H:\mathbb{U} \to \mathbb{V}` which takes in an object :math:`f \in \mathbb{U}` and maps it to corresponding projections :math:`g \in \mathbb{V}` that would be produced by the imaging system. A system matrix consists of sequences of object-to-object and proj-to-proj transforms that model various characteristics of the imaging system, such as attenuation and blurring. While the class implements the operator :math:`H:\mathbb{U} \to \mathbb{V}` through the ``forward`` method, it also implements :math:`H^T:\mathbb{V} \to \mathbb{U}` through the `backward` method, required during iterative reconstruction algorithms such as OSEM.

   :param obj2obj_transforms: Sequence of object mappings that occur before forward projection.
   :type obj2obj_transforms: Sequence[Transform]
   :param im2im_transforms: Sequence of proj mappings that occur after forward projection.
   :type im2im_transforms: Sequence[Transform]
   :param object_meta: Object metadata.
   :type object_meta: ObjectMeta
   :param proj_meta: Projection metadata.
   :type proj_meta: ProjMeta

   .. py:method:: forward(object, subset_idx = None)

      Forward transform :math:`H' = \sum_n v_n \otimes B_n H_n A_n`, This adds an additional dimension to the projection space.

      :param object: Object to be forward projected. Must have a batch size of 1.
      :type object: torch.Tensor[1,Lx,Ly,Lz]
      :param angle_subset: Only uses a subset of angles (i.e. only certain values of :math:`j` in formula above) when back projecting. Useful for ordered-subset reconstructions. Defaults to None, which assumes all angles are used.
      :type angle_subset: Sequence[int], optional

      :returns: Forward projection.
      :rtype: torch.Tensor[N_gates,...]


   .. py:method:: backward(proj, subset_idx = None)

      Back projection :math:`H' = \sum_n v_n^T \otimes A_n^T H_n^T B_n^T`. This maps an extended projection back to the original object space.

      :param proj: Projection data to be back-projected.
      :type proj: torch.Tensor[N,...]
      :param angle_subset: Only uses a subset of angles (i.e. only certain values of :math:`j` in formula above) when back projecting. Useful for ordered-subset reconstructions. Defaults to None, which assumes all angles are used.. Defaults to None.
      :type angle_subset: Sequence[int], optional

      :returns: Back projection.
      :rtype: torch.Tensor[1,Lx,Ly,Lz]


   .. py:method:: set_n_subsets(n_subsets)


   .. py:method:: get_projection_subset(projections, subset_idx)


   .. py:method:: compute_normalization_factor(subset_idx = None)

      Function called by reconstruction algorithms to get the normalization factor :math:`H' = \sum_n v_n^T \otimes A_n^T H_n^T B_n^T` 1.

      :returns: Normalization factor.
      :rtype: torch.Tensor[1,Lx,Ly,Lz]



