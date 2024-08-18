:py:mod:`pytomography.utils`
============================

.. py:module:: pytomography.utils

.. autoapi-nested-parse::

   This module contains utility functions used in the other modules of PyTomography



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   fourier_filters/index.rst
   misc/index.rst
   nist_data/index.rst
   scatter/index.rst
   spatial/index.rst
   sss/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   pytomography.utils.HammingFilter
   pytomography.utils.RampFilter



Functions
~~~~~~~~~

.. autoapisummary::

   pytomography.utils.rev_cumsum
   pytomography.utils.get_distance
   pytomography.utils.get_object_nearest_neighbour
   pytomography.utils.print_collimator_parameters
   pytomography.utils.check_if_class_contains_method
   pytomography.utils.get_1d_gaussian_kernel
   pytomography.utils.rotate_detector_z
   pytomography.utils.compute_pad_size
   pytomography.utils.pad_proj
   pytomography.utils.pad_object
   pytomography.utils.unpad_proj
   pytomography.utils.unpad_object
   pytomography.utils.pad_object_z
   pytomography.utils.unpad_object_z
   pytomography.utils.dual_sqrt_exponential
   pytomography.utils.get_E_mu_data_from_datasheet
   pytomography.utils.get_mu_from_spectrum_interp
   pytomography.utils.compute_EW_scatter



.. py:function:: rev_cumsum(x)

   Reverse cumulative sum along the first axis of a tensor of shape [Lx, Ly, Lz].
   since this is used with SPECT attenuation correction, the initial voxel only contributes 1/2.

   :param x: Tensor to be summed
   :type x: torch.tensor[Lx,Ly,Lz]

   :returns: The cumulatively summed tensor.
   :rtype: torch.tensor[Lx, Ly, Lz]


.. py:function:: get_distance(Lx, r, dx)

   Given the radial distance to center of object space from the scanner, computes the distance between each parallel plane (i.e. (y-z plane)) and a detector located at +x. This function is used for SPECT PSF modeling where the amount of blurring depends on thedistance from the detector.

   :param Lx: The number of y-z planes to compute the distance of
   :type Lx: int
   :param r: The radial distance between the central y-z plane and the detector at +x.
   :type r: float
   :param dx: The spacing between y-z planes in Euclidean distance.
   :type dx: float

   :returns: An array of distances for each y-z plane to the detector.
   :rtype: np.array[Lx]


.. py:function:: get_object_nearest_neighbour(object, shifts, mode='replicate')

   Given an object tensor, finds the nearest neighbour (corresponding to ``shifts``) for each voxel (done by shifting object by i,j,k)

   :param object: Original object
   :type object: torch.Tensor
   :param shifts: List of three integers [i,j,k] corresponding to neighbour location
   :type shifts: list[int]

   :returns: Shifted object whereby each voxel corresponding to neighbour [i,j,k] of the ``object``.
   :rtype: torch.Tensor


.. py:function:: print_collimator_parameters()

   Prints all the available SPECT collimator parameters



.. py:function:: check_if_class_contains_method(instance, method_name)

   Checks if class corresponding to instance implements the method ``method_name``

   :param instance: A python object
   :type instance: Object
   :param method_name: Name of the method of the object being checked
   :type method_name: str


.. py:function:: get_1d_gaussian_kernel(sigma, kernel_size, padding_mode='zeros')

   Returns a 1D gaussian blurring kernel

   :param sigma: Sigma (in pixels) of blurring pixels
   :type sigma: float
   :param kernel_size: Size of kernel used
   :type kernel_size: int
   :param padding_mode: Type of padding. Defaults to 'zeros'.
   :type padding_mode: str, optional

   :returns: Torch Conv1d layer corresponding to the gaussian kernel
   :rtype: Conv1d


.. py:function:: rotate_detector_z(x, angles, mode = 'bilinear', negative = False)

   Returns an object tensor in a rotated reference frame such that the scanner is located at the +x axis. Note that the scanner angle :math:`\beta` is related to :math:`\phi` (azimuthal angle) by :math:`\phi = 3\pi/2 - \beta`.

   :param x: Tensor aligned with cartesian coordinate system specified
   :type x: torch.tensor[batch_size, Lx, Ly, Lz]
   :param by the manual.:
   :param angles: The angles :math:`\beta` where the scanner is located for each element in the batch x.
   :type angles: torch.Tensor
   :param mode: Method of interpolation used to get rotated object. Defaults to bilinear.
   :type mode: str, optional
   :param negative: If True, applies an inverse rotation. In this case, the tensor
   :type negative: bool, optional
   :param x is an object in a coordinate system aligned with :math:`\beta`:
   :param and the function rotates the:
   :param x back to the original cartesian coordinate system specified by the users manual. In particular:
   :param if one:
   :param uses this function on a tensor with negative=False:
   :param then applies this function to that returned:
   :param tensor with negative=True:
   :param it should return the same tensor. Defaults to False.:

   :returns: Rotated tensor.
   :rtype: torch.tensor[batch_size, Lx, Ly, Lz]


.. py:function:: compute_pad_size(width)

   Computes the pad width required such that subsequent rotation retains the entire object

   :param width: width of the corresponding axis (i.e. number of elements in the dimension)
   :type width: int

   :returns: the number of pixels by which the axis needs to be padded on each side
   :rtype: int


.. py:function:: pad_proj(proj, mode = 'constant', value = 0)

   Pads projections along the Lr axis

   :param proj: Projections tensor.
   :type proj: torch.Tensor[batch_size, Ltheta, Lr, Lz]
   :param mode: Padding mode to use. Defaults to 'constant'.
   :type mode: str, optional
   :param value: If padding mode is constant, fill with this value. Defaults to 0.
   :type value: float, optional

   :returns: Padded projections tensor.
   :rtype: torch.Tensor[batch_size, Ltheta, Lr', Lz]


.. py:function:: pad_object(object, mode='constant')

   Pads object tensors by enough pixels in the xy plane so that subsequent rotations don't crop out any of the object

   :param object: object tensor to be padded
   :type object: torch.Tensor[batch_size, Lx, Ly, Lz]
   :param mode: _description_. Defaults to 'constant'.
   :type mode: str, optional

   :returns: _description_
   :rtype: _type_


.. py:function:: unpad_proj(proj)

   Unpads the projections back to original Lr dimensions

   :param proj: Padded projections tensor
   :type proj: torch.Tensor[batch_size, Ltheta, Lr', Lz]

   :returns: Unpadded projections tensor
   :rtype: torch.Tensor[batch_size, Ltheta, Lr, Lz]


.. py:function:: unpad_object(object)

   Unpads a padded object tensor in the xy plane back to its original dimensions

   :param object: padded object tensor
   :type object: torch.Tensor[batch_size, Lx', Ly', Lz]

   :returns: Object tensor back to it's original dimensions.
   :rtype: torch.Tensor[batch_size, Lx, Ly, Lz]


.. py:function:: pad_object_z(object, pad_size, mode='constant')

   Pads an object tensor along z. Useful for PSF modeling

   :param object: Object tensor
   :type object: torch.Tensor[batch_size, Lx, Ly, Lz]
   :param pad_size: Amount by which to pad in -z and +z
   :type pad_size: int
   :param mode: Padding mode. Defaults to 'constant'.
   :type mode: str, optional

   :returns: Padded object tensor along z.
   :rtype: torch.Tensor[torch.Tensor[batch_size, Lx, Ly, Lz']]


.. py:function:: unpad_object_z(object, pad_size)

   Unpads an object along the z dimension

   :param object: Padded object tensor along z.
   :type object: torch.Tensor[batch_size, Lx, Ly, Lz']
   :param pad_size: Amount by which the padded tensor was padded in the z direcion
   :type pad_size: int

   :returns: Unpadded object tensor.
   :rtype: torch.Tensor[batch_size, Lx, Ly, Lz]


.. py:function:: dual_sqrt_exponential(energy, c1, c2, d1, d2)

   Function used for curve fitting of linear attenuation coefficient vs. photon energy curves from NIST. It's given by the functional form :math:`f(x) = c_1e^{-d_1\sqrt{x}} + c_2e^{-d_2\sqrt{x}}`. It was chosen purely because it gave good fit results.

   :param energy: Energy of photon
   :type energy: float
   :param c1: Fit parameter 1
   :type c1: float
   :param c2: Fit parameter 2
   :type c2: float
   :param d1: Fit parameter 3
   :type d1: float
   :param d2: Fit parameter 4
   :type d2: float

   :returns: _description_
   :rtype: float


.. py:function:: get_E_mu_data_from_datasheet(file)

   Return energy and linear attenuation data from NIST datafiles of mass attenuation coefficients between 50keV and 511keV.

   :param file: Location of NIST data file. Corresponds to a particular element/material.
   :type file: str

   :returns: Energy and linear attenuation values.
   :rtype: tuple[np.array, np.array]


.. py:function:: get_mu_from_spectrum_interp(file, energy)

   Gets linear attenuation corresponding to a given energy in in the data from ``file``.

   :param file: Filepath of the mu-energy data
   :type file: str
   :param energy: Energy at which mu is computed
   :type energy: float

   :returns: Linear attenuation coefficient (in 1/cm) at the desired energies.
   :rtype: np.array


.. py:function:: compute_EW_scatter(projection_lower, projection_upper, width_lower, width_upper, width_peak, weighting_lower = 0.5, weighting_upper = 0.5, proj_meta=None, sigma_theta = 0, sigma_r = 0, sigma_z = 0, N_sigmas = 3, return_scatter_variance_estimate = False)

   Computes triple energy window estimate from lower and upper scatter projections as well as window widths

   :param projection_lower: Projection data corresponding to lower energy window
   :type projection_lower: torch.Tensor
   :param projection_upper: Projection data corresponding to upper energy window
   :type projection_upper: torch.Tensor
   :param width_lower: Width of lower energy window
   :type width_lower: float
   :param width_upper: Width of upper energy window
   :type width_upper: float
   :param width_peak: Width of peak energy window
   :type width_peak: float
   :param return_scatter_variance_estimate: Return scatter variance estimate. Defaults to False.
   :type return_scatter_variance_estimate: bool, optional

   :returns: Scatter estimate (and scatter variance estimate if specified)
   :rtype: torch.Tensor | Sequence[torch.Tensor]


.. py:class:: HammingFilter(wl, wh)

   Implementation of the Hamming filter given by :math:`\Pi(\omega) = \frac{1}{2}\left(1+\cos\left(\frac{\pi(|\omega|-\omega_L)}{\omega_H-\omega_L} \right)\right)` for :math:`\omega_L \leq |\omega| < \omega_H` and :math:`\Pi(\omega) = 1` for :math:`|\omega| \leq \omega_L` and :math:`\Pi(\omega) = 0` for :math:`|\omega|>\omega_H`. Arguments ``wl`` and ``wh`` should be expressed as fractions of the Nyquist frequency (i.e. ``wh=0.93`` represents 93% the Nyquist frequency).


   .. py:method:: __call__(w)



.. py:class:: RampFilter

   Implementation of the Ramp filter :math:`\Pi(\omega) = |\omega|`


   .. py:method:: __call__(w)



