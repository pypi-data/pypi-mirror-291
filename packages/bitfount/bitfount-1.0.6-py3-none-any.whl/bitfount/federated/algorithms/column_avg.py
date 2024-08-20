"""Column averaging algorithm."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, Mapping, Optional

from marshmallow import fields
import numpy as np
import numpy.typing as npt

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the ColumnAverage algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(
        self, results: Mapping[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the ColumnAverage algorithm."""

    def __init__(self, *, field: str, table_name: str, **kwargs: Any) -> None:
        self.datasource: BaseSource
        self.field = field
        self.table_name = table_name
        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.initialise_data(datasource=datasource)

    def run(self, **kwargs: Any) -> Dict[str, npt.NDArray[np.float64]]:
        """Returns the mean of the field in `BaseSource` dataframe."""
        mean = np.mean(
            self.datasource.get_column(col_name=self.field, table_name=self.table_name)
        )
        return {"mean": np.array(mean)}


@delegates()
class ColumnAverage(BaseAlgorithmFactory):
    """Simple algorithm for taking the arithmetic mean of a column in a table.

    Args:
        field: The name of the column to take the mean of.
        table_name: The name of the table on which column
            average will be performed on.

    Attributes:
        field: The name of the column to take the mean of.
        table_name: The name of the table on which column
            average will be performed on.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "field": fields.Str(required=True),
        "table_name": fields.Str(required=True),
    }
    _inference_algorithm: bool = False

    def __init__(self, *, field: str, table_name: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.field = field
        self.table_name = table_name

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ColumnAverage algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the ColumnAverage algorithm."""
        return _WorkerSide(field=self.field, table_name=self.table_name, **kwargs)
