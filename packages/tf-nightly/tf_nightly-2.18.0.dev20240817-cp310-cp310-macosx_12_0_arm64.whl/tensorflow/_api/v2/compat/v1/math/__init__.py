# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.math namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.math import special
from tensorflow.python.ops.gen_array_ops import invert_permutation # line: 4634
from tensorflow.python.ops.gen_math_ops import acosh # line: 231
from tensorflow.python.ops.gen_math_ops import asin # line: 991
from tensorflow.python.ops.gen_math_ops import asinh # line: 1091
from tensorflow.python.ops.gen_math_ops import atan # line: 1184
from tensorflow.python.ops.gen_math_ops import atan2 # line: 1284
from tensorflow.python.ops.gen_math_ops import atanh # line: 1383
from tensorflow.python.ops.gen_math_ops import betainc # line: 1844
from tensorflow.python.ops.gen_math_ops import cos # line: 2521
from tensorflow.python.ops.gen_math_ops import cosh # line: 2615
from tensorflow.python.ops.gen_math_ops import digamma # line: 3218
from tensorflow.python.ops.gen_math_ops import erf # line: 3511
from tensorflow.python.ops.gen_math_ops import erfc # line: 3603
from tensorflow.python.ops.gen_math_ops import expm1 # line: 3904
from tensorflow.python.ops.gen_math_ops import floor_mod as floormod # line: 4149
from tensorflow.python.ops.gen_math_ops import greater # line: 4243
from tensorflow.python.ops.gen_math_ops import greater_equal # line: 4344
from tensorflow.python.ops.gen_math_ops import igamma # line: 4537
from tensorflow.python.ops.gen_math_ops import igammac # line: 4696
from tensorflow.python.ops.gen_math_ops import is_finite # line: 4992
from tensorflow.python.ops.gen_math_ops import is_inf # line: 5088
from tensorflow.python.ops.gen_math_ops import is_nan # line: 5184
from tensorflow.python.ops.gen_math_ops import less # line: 5280
from tensorflow.python.ops.gen_math_ops import less_equal # line: 5381
from tensorflow.python.ops.gen_math_ops import lgamma # line: 5482
from tensorflow.python.ops.gen_math_ops import log # line: 5652
from tensorflow.python.ops.gen_math_ops import log1p # line: 5746
from tensorflow.python.ops.gen_math_ops import logical_and # line: 5836
from tensorflow.python.ops.gen_math_ops import logical_not # line: 5975
from tensorflow.python.ops.gen_math_ops import logical_or # line: 6062
from tensorflow.python.ops.gen_math_ops import maximum # line: 6383
from tensorflow.python.ops.gen_math_ops import minimum # line: 6639
from tensorflow.python.ops.gen_math_ops import floor_mod as mod # line: 4149
from tensorflow.python.ops.gen_math_ops import neg as negative # line: 6986
from tensorflow.python.ops.gen_math_ops import next_after as nextafter # line: 7072
from tensorflow.python.ops.gen_math_ops import polygamma # line: 7240
from tensorflow.python.ops.gen_math_ops import reciprocal # line: 8232
from tensorflow.python.ops.gen_math_ops import rint # line: 8729
from tensorflow.python.ops.gen_math_ops import segment_max # line: 9003
from tensorflow.python.ops.gen_math_ops import segment_mean # line: 9237
from tensorflow.python.ops.gen_math_ops import segment_min # line: 9362
from tensorflow.python.ops.gen_math_ops import segment_prod # line: 9596
from tensorflow.python.ops.gen_math_ops import segment_sum # line: 9822
from tensorflow.python.ops.gen_math_ops import sin # line: 10372
from tensorflow.python.ops.gen_math_ops import sinh # line: 10465
from tensorflow.python.ops.gen_math_ops import square # line: 12035
from tensorflow.python.ops.gen_math_ops import squared_difference # line: 12124
from tensorflow.python.ops.gen_math_ops import tan # line: 12425
from tensorflow.python.ops.gen_math_ops import tanh # line: 12519
from tensorflow.python.ops.gen_math_ops import unsorted_segment_max # line: 12862
from tensorflow.python.ops.gen_math_ops import unsorted_segment_min # line: 13000
from tensorflow.python.ops.gen_math_ops import unsorted_segment_prod # line: 13134
from tensorflow.python.ops.gen_math_ops import unsorted_segment_sum # line: 13268
from tensorflow.python.ops.gen_math_ops import xlogy # line: 13517
from tensorflow.python.ops.gen_math_ops import zeta # line: 13603
from tensorflow.python.ops.gen_nn_ops import softsign # line: 12232
from tensorflow.python.ops.bincount_ops import bincount_v1 as bincount # line: 190
from tensorflow.python.ops.check_ops import is_non_decreasing # line: 1996
from tensorflow.python.ops.check_ops import is_strictly_increasing # line: 2037
from tensorflow.python.ops.confusion_matrix import confusion_matrix_v1 as confusion_matrix # line: 199
from tensorflow.python.ops.math_ops import abs # line: 361
from tensorflow.python.ops.math_ops import accumulate_n # line: 3987
from tensorflow.python.ops.math_ops import acos # line: 5799
from tensorflow.python.ops.math_ops import add # line: 3846
from tensorflow.python.ops.math_ops import add_n # line: 3927
from tensorflow.python.ops.math_ops import angle # line: 865
from tensorflow.python.ops.math_ops import argmax # line: 247
from tensorflow.python.ops.math_ops import argmin # line: 301
from tensorflow.python.ops.math_ops import ceil # line: 5629
from tensorflow.python.ops.math_ops import conj # line: 4360
from tensorflow.python.ops.math_ops import count_nonzero # line: 2280
from tensorflow.python.ops.math_ops import cumprod # line: 4250
from tensorflow.python.ops.math_ops import cumsum # line: 4178
from tensorflow.python.ops.math_ops import cumulative_logsumexp # line: 4304
from tensorflow.python.ops.math_ops import divide # line: 442
from tensorflow.python.ops.math_ops import div_no_nan as divide_no_nan # line: 1526
from tensorflow.python.ops.math_ops import equal # line: 1790
from tensorflow.python.ops.math_ops import erfcinv # line: 5599
from tensorflow.python.ops.math_ops import erfinv # line: 5564
from tensorflow.python.ops.math_ops import exp # line: 5696
from tensorflow.python.ops.math_ops import floor # line: 5830
from tensorflow.python.ops.math_ops import floordiv # line: 1634
from tensorflow.python.ops.math_ops import imag # line: 831
from tensorflow.python.ops.math_ops import log_sigmoid # line: 4133
from tensorflow.python.ops.math_ops import logical_xor # line: 1714
from tensorflow.python.ops.math_ops import multiply # line: 477
from tensorflow.python.ops.math_ops import multiply_no_nan # line: 1581
from tensorflow.python.ops.math_ops import ndtri # line: 5583
from tensorflow.python.ops.math_ops import not_equal # line: 1827
from tensorflow.python.ops.math_ops import polyval # line: 5386
from tensorflow.python.ops.math_ops import pow # line: 665
from tensorflow.python.ops.math_ops import real # line: 790
from tensorflow.python.ops.math_ops import reciprocal_no_nan # line: 5458
from tensorflow.python.ops.math_ops import reduce_all_v1 as reduce_all # line: 3036
from tensorflow.python.ops.math_ops import reduce_any_v1 as reduce_any # line: 3142
from tensorflow.python.ops.math_ops import reduce_euclidean_norm # line: 2235
from tensorflow.python.ops.math_ops import reduce_logsumexp_v1 as reduce_logsumexp # line: 3248
from tensorflow.python.ops.math_ops import reduce_max_v1 as reduce_max # line: 2911
from tensorflow.python.ops.math_ops import reduce_mean_v1 as reduce_mean # line: 2434
from tensorflow.python.ops.math_ops import reduce_min_v1 as reduce_min # line: 2783
from tensorflow.python.ops.math_ops import reduce_prod_v1 as reduce_prod # line: 2724
from tensorflow.python.ops.math_ops import reduce_std # line: 2624
from tensorflow.python.ops.math_ops import reduce_sum_v1 as reduce_sum # line: 2077
from tensorflow.python.ops.math_ops import reduce_variance # line: 2561
from tensorflow.python.ops.math_ops import round # line: 910
from tensorflow.python.ops.math_ops import rsqrt # line: 5774
from tensorflow.python.ops.math_ops import scalar_mul # line: 588
from tensorflow.python.ops.math_ops import sigmoid # line: 4080
from tensorflow.python.ops.math_ops import sign # line: 743
from tensorflow.python.ops.math_ops import sobol_sample # line: 5749
from tensorflow.python.ops.math_ops import softplus # line: 630
from tensorflow.python.ops.math_ops import sqrt # line: 5657
from tensorflow.python.ops.math_ops import subtract # line: 541
from tensorflow.python.ops.math_ops import truediv # line: 1460
from tensorflow.python.ops.math_ops import unsorted_segment_mean # line: 4483
from tensorflow.python.ops.math_ops import unsorted_segment_sqrt_n # line: 4538
from tensorflow.python.ops.math_ops import xdivy # line: 5492
from tensorflow.python.ops.math_ops import xlog1py # line: 5526
from tensorflow.python.ops.nn_impl import l2_normalize # line: 540
from tensorflow.python.ops.nn_impl import zero_fraction # line: 620
from tensorflow.python.ops.nn_ops import approx_max_k # line: 5882
from tensorflow.python.ops.nn_ops import approx_min_k # line: 5945
from tensorflow.python.ops.nn_ops import in_top_k # line: 6532
from tensorflow.python.ops.nn_ops import log_softmax # line: 3923
from tensorflow.python.ops.nn_ops import softmax # line: 3910
from tensorflow.python.ops.nn_ops import top_k # line: 5815
from tensorflow.python.ops.special_math_ops import bessel_i0 # line: 253
from tensorflow.python.ops.special_math_ops import bessel_i0e # line: 282
from tensorflow.python.ops.special_math_ops import bessel_i1 # line: 309
from tensorflow.python.ops.special_math_ops import bessel_i1e # line: 338
from tensorflow.python.ops.special_math_ops import lbeta # line: 45

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "math", public_apis=None, deprecation=False,
      has_lite=False)
