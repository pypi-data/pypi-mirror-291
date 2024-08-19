from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from titantic_classification.config.core import config
from titantic_classification.processing.data_manager import clean_dataset


def drop_irrelevant_vars(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    validated_data.drop(
        labels=config.model_config.variables_to_drop, axis=1, inplace=True
    )
    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)
    input_data = clean_dataset(dataframe=input_data)
    validated_data = input_data[config.model_config.features].copy()
    errors = None
    try:
        # replace numpy nans so that pydantic can validate
        MultipleTitanticDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        print(f"Validation error: {error}")
        errors = error.json()

    return validated_data, errors


class TitanticSurvivorInput(BaseModel):
    pclass: Optional[int]
    name: Optional[str]
    sex: Optional[str]
    age: Optional[int]
    sibsp: Optional[int]
    parch: Optional[int]
    ticket: Optional[int]
    fare: Optional[float]
    cabin: Optional[str]
    embarked: Optional[str]
    boat: Optional[Union[str, int]]
    body: Optional[int]


class MultipleTitanticDataInputs(BaseModel):
    inputs: List[TitanticSurvivorInput]
