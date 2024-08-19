from titantic_classification.config.core import config
from titantic_classification.processing.features import ExtractLetterTransformer


def test_temporal_variable_transformer(sample_input_data):
    # Given
    transformer = ExtractLetterTransformer(
        variables=config.model_config.cabin_vars,
    )

    assert sample_input_data["cabin"].iat[6] == "E12"

    # When
    subject = transformer.fit_transform(sample_input_data)

    # Then
    assert subject["cabin"].iat[6] == "E"
