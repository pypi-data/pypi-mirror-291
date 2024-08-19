import numpy as np
from sklearn.metrics import accuracy_score

from titantic_classification import __version__ as _version
from titantic_classification.predict import make_prediction


def test_make_prediction(sample_input_data):
    expected_no_predictions = 131

    result = make_prediction(input_data=sample_input_data)

    predictions = result.get("predictions")
    assert len(predictions) == expected_no_predictions
    assert result.get("errors") is None
    assert result.get("version") == _version
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    _predictions = list(predictions)
    y_true = sample_input_data["survived"]
    accuracy = accuracy_score(_predictions, y_true)
    assert accuracy > 0.7
    print("Accuracy:", accuracy)
