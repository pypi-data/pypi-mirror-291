# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.data.experimental namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.data.experimental import service
from tensorflow.python.data.experimental.ops.batching import dense_to_ragged_batch # line: 30
from tensorflow.python.data.experimental.ops.batching import dense_to_sparse_batch # line: 94
from tensorflow.python.data.experimental.ops.batching import map_and_batch # line: 210
from tensorflow.python.data.experimental.ops.batching import map_and_batch_with_legacy_function # line: 146
from tensorflow.python.data.experimental.ops.batching import unbatch # line: 269
from tensorflow.python.data.experimental.ops.cardinality import INFINITE as INFINITE_CARDINALITY # line: 26
from tensorflow.python.data.experimental.ops.cardinality import UNKNOWN as UNKNOWN_CARDINALITY # line: 28
from tensorflow.python.data.experimental.ops.cardinality import assert_cardinality # line: 67
from tensorflow.python.data.experimental.ops.cardinality import cardinality # line: 33
from tensorflow.python.data.experimental.ops.counter import CounterV1 as Counter # line: 62
from tensorflow.python.data.experimental.ops.distribute import SHARD_HINT # line: 31
from tensorflow.python.data.experimental.ops.distributed_save_op import distributed_save # line: 28
from tensorflow.python.data.experimental.ops.enumerate_ops import enumerate_dataset # line: 21
from tensorflow.python.data.experimental.ops.error_ops import ignore_errors # line: 20
from tensorflow.python.data.experimental.ops.from_list import from_list # line: 75
from tensorflow.python.data.experimental.ops.get_single_element import get_single_element # line: 22
from tensorflow.python.data.experimental.ops.grouping import Reducer # line: 388
from tensorflow.python.data.experimental.ops.grouping import bucket_by_sequence_length # line: 112
from tensorflow.python.data.experimental.ops.grouping import group_by_reducer # line: 28
from tensorflow.python.data.experimental.ops.grouping import group_by_window # line: 59
from tensorflow.python.data.experimental.ops.interleave_ops import choose_from_datasets_v1 as choose_from_datasets # line: 233
from tensorflow.python.data.experimental.ops.interleave_ops import parallel_interleave # line: 29
from tensorflow.python.data.experimental.ops.interleave_ops import sample_from_datasets_v1 as sample_from_datasets # line: 158
from tensorflow.python.data.experimental.ops.iterator_ops import get_model_proto # line: 103
from tensorflow.python.data.experimental.ops.iterator_ops import make_saveable_from_iterator # line: 41
from tensorflow.python.data.experimental.ops.lookup_ops import DatasetInitializer # line: 54
from tensorflow.python.data.experimental.ops.lookup_ops import index_table_from_dataset # line: 190
from tensorflow.python.data.experimental.ops.lookup_ops import table_from_dataset # line: 102
from tensorflow.python.data.experimental.ops.pad_to_cardinality import pad_to_cardinality # line: 26
from tensorflow.python.data.experimental.ops.parsing_ops import parse_example_dataset # line: 105
from tensorflow.python.data.experimental.ops.prefetching_ops import copy_to_device # line: 65
from tensorflow.python.data.experimental.ops.prefetching_ops import prefetch_to_device # line: 33
from tensorflow.python.data.experimental.ops.random_ops import RandomDatasetV1 as RandomDataset # line: 34
from tensorflow.python.data.experimental.ops.readers import CsvDatasetV1 as CsvDataset # line: 824
from tensorflow.python.data.experimental.ops.readers import SqlDatasetV1 as SqlDataset # line: 1202
from tensorflow.python.data.experimental.ops.readers import make_batched_features_dataset_v1 as make_batched_features_dataset # line: 1099
from tensorflow.python.data.experimental.ops.readers import make_csv_dataset_v1 as make_csv_dataset # line: 629
from tensorflow.python.data.experimental.ops.resampling import rejection_resample # line: 21
from tensorflow.python.data.experimental.ops.scan_ops import scan # line: 21
from tensorflow.python.data.experimental.ops.shuffle_ops import shuffle_and_repeat # line: 62
from tensorflow.python.data.experimental.ops.snapshot import snapshot # line: 190
from tensorflow.python.data.experimental.ops.take_while_ops import take_while # line: 21
from tensorflow.python.data.experimental.ops.unique import unique # line: 21
from tensorflow.python.data.experimental.ops.writers import TFRecordWriter # line: 27
from tensorflow.python.data.ops.dataset_ops import AUTOTUNE # line: 105
from tensorflow.python.data.ops.dataset_ops import DatasetSpec as DatasetStructure # line: 4585
from tensorflow.python.data.ops.dataset_ops import from_variant # line: 4557
from tensorflow.python.data.ops.dataset_ops import get_structure # line: 4392
from tensorflow.python.data.ops.dataset_ops import to_variant # line: 4572
from tensorflow.python.data.ops.debug_mode import enable_debug_mode # line: 24
from tensorflow.python.data.ops.iterator_ops import get_next_as_optional # line: 1015
from tensorflow.python.data.ops.optional_ops import Optional # line: 31
from tensorflow.python.data.ops.optional_ops import OptionalSpec as OptionalStructure # line: 205
from tensorflow.python.data.ops.options import AutoShardPolicy # line: 88
from tensorflow.python.data.ops.options import AutotuneAlgorithm # line: 30
from tensorflow.python.data.ops.options import AutotuneOptions # line: 193
from tensorflow.python.data.ops.options import DistributeOptions # line: 278
from tensorflow.python.data.ops.options import ExternalStatePolicy # line: 155
from tensorflow.python.data.ops.options import OptimizationOptions # line: 320
from tensorflow.python.data.ops.options import ThreadingOptions # line: 479
from tensorflow.python.data.util.structure import _RaggedTensorStructure as RaggedTensorStructure # line: 61
from tensorflow.python.data.util.structure import _SparseTensorStructure as SparseTensorStructure # line: 48
from tensorflow.python.data.util.structure import _TensorArrayStructure as TensorArrayStructure # line: 54
from tensorflow.python.data.util.structure import _TensorStructure as TensorStructure # line: 42
from tensorflow.python.framework.type_spec import TypeSpec as Structure # line: 49

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "data.experimental", public_apis=None, deprecation=False,
      has_lite=False)
