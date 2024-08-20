from collections import OrderedDict
from collections.abc import Generator
from enum import auto
from typing import Any

import tensorflow as tf
from loguru import logger

from kdp.features import (
    CategoricalFeature,
    CategoryEncodingOptions,
    DateFeature,
    Feature,
    FeatureType,
    NumericalFeature,
    TextFeature,
)
from kdp.layers_factory import PreprocessorLayerFactory
from kdp.pipeline import FeaturePreprocessor
from kdp.stats import DatasetStatistics


class OutputModeOptions(auto):
    CONCAT = "concat"
    DICT = "dict"


class TextVectorizerOutputOptions(auto):
    TF_IDF = "tf_idf"
    INT = "int"
    MULTI_HOT = "multi_hot"


class TransformerBlockPlacementOptions(auto):
    CATEGORICAL = "categorical"
    ALL_FEATURES = "all_features"


class FeatureSpaceConverter:
    def __init__(self):
        """Initialize the FeatureSpaceConverter class."""
        self.features_space = {}
        self.numeric_features = []
        self.categorical_features = []
        self.text_features = []
        self.date_features = []  # Add date_features list

    def _init_features_specs(self, features_specs: dict) -> None:
        """Format the features space into a dictionary.

        Args:
            features_specs (dict): A dictionary with the features and their types,
            where types can be specified as either FeatureType enums,
            class instances (NumericalFeature, CategoricalFeature, TextFeature), or strings.
        """
        for name, spec in features_specs.items():
            # Direct instance check for standard pipelines
            if isinstance(spec, NumericalFeature | CategoricalFeature | TextFeature | DateFeature):
                feature_instance = spec
            else:
                # handling custom features pipelines
                if isinstance(spec, Feature):
                    feature_type = spec.feature_type
                else:
                    # Convert string to FeatureType if necessary
                    feature_type = FeatureType[spec.upper()] if isinstance(spec, str) else spec

                # Creating feature objects based on type
                if feature_type in {
                    FeatureType.FLOAT,
                    FeatureType.FLOAT_NORMALIZED,
                    FeatureType.FLOAT_RESCALED,
                    FeatureType.FLOAT_DISCRETIZED,
                }:
                    feature_instance = NumericalFeature(name=name, feature_type=feature_type)
                elif feature_type in {FeatureType.INTEGER_CATEGORICAL, FeatureType.STRING_CATEGORICAL}:
                    feature_instance = CategoricalFeature(name=name, feature_type=feature_type)
                elif feature_type == FeatureType.TEXT:
                    feature_instance = TextFeature(name=name, feature_type=feature_type)
                elif feature_type == FeatureType.DATE:
                    feature_instance = DateFeature(name=name, feature_type=feature_type)
                else:
                    raise ValueError(f"Unsupported feature type for feature '{name}': {spec}")

            # Adding custom pipelines
            if isinstance(spec, Feature):
                logger.info(f"Adding custom preprocessors to the object: {spec.preprocessors}")
                feature_instance.preprocessors = spec.preprocessors
                feature_instance.kwargs = spec.kwargs

            # Categorize feature based on its class
            if isinstance(feature_instance, NumericalFeature):
                self.numeric_features.append(name)
            elif isinstance(feature_instance, CategoricalFeature):
                self.categorical_features.append(name)
            elif isinstance(feature_instance, TextFeature):
                self.text_features.append(name)
            elif isinstance(feature_instance, DateFeature):
                self.date_features.append(name)

            # Adding formatted spec to the features_space dictionary
            self.features_space[name] = feature_instance

        return self.features_space


class PreprocessingModel:
    def __init__(
        self,
        features_stats: dict[str, Any] = None,
        path_data: str = None,
        batch_size: int = 50_000,
        feature_crosses: list[tuple[str, str, int]] = None,
        features_stats_path: str = None,
        output_mode: str = OutputModeOptions.CONCAT,
        overwrite_stats: bool = False,
        log_to_file: bool = False,
        features_specs: dict[str, FeatureType | str] = None,
        transfo_nr_blocks: int = None,
        transfo_nr_heads: int = 3,
        transfo_ff_units: int = 16,
        transfo_dropout_rate: float = 0.25,
        transfo_placement: str = TransformerBlockPlacementOptions.CATEGORICAL,
    ) -> None:
        """Initialize a preprocessing model.

        Args:
            features_stats (dict[str, Any]): A dictionary containing the statistics of the features.
            path_data (str): The path to the data from which estimate the statistics.
            batch_size (int): The batch size for the data iteration for stats estimation.
            feature_crosses (list[tuple[str, str, int]]):
                A list of tuples containing the names of the features to be crossed,
                and nr_bins to be used for hashing.
            features_stats_path (str): The path where to save/load features statistics.
            output_mode (str): The output mode of the model (concat | dict).
            overwrite_stats (bool): A boolean indicating whether to overwrite the statistics.
            log_to_file (bool): A boolean indicating whether to log to a file.
            features_specs (dict[str, FeatureType | str]): A dictionary containing the features and their types.
            transfo_nr_blocks (int): The number of transformer blocks for the transformer block
                (default=None, transformer block is disabled).
            transfo_nr_heads (int): The number of heads for the transformer block (categorical variables).
            transfo_ff_units (int): The number of feed forward units for the transformer
            transfo_dropout_rate (float): The dropout rate for the transformer block (default=0.25).
            transfo_placement (str): The placement of the transformer block (categorical | all_features).
        """
        self.path_data = path_data
        self.batch_size = batch_size or 50_000
        self.features_stats = features_stats or {}
        self.features_specs = features_specs or {}
        self.features_stats_path = features_stats_path or "features_stats.json"
        self.feature_crosses = feature_crosses or []
        self.output_mode = output_mode
        self.overwrite_stats = overwrite_stats
        # transformer blocks controll
        self.transfo_nr_blocks = transfo_nr_blocks
        self.transfo_nr_heads = transfo_nr_heads
        self.transfo_ff_units = transfo_ff_units
        self.transfo_dropout_rate = transfo_dropout_rate
        self.transfo_placement = transfo_placement

        # PLACEHOLDERS
        self.preprocessors = {}
        self.inputs = {}
        self.signature = {}
        self.outputs = {}
        self.outputs_categorical = {}

        if log_to_file:
            logger.info("Logging to file enabled 🗂️")
            logger.add("PreprocessModel.log")

        # formatting features specs info
        self._init_features_specs(features_specs=features_specs)

        # initializing stats
        self._init_stats()

    def _init_features_specs(self, features_specs: dict) -> None:
        """Format the features space into a dictionary.

        Args:
            features_specs (dict): A dictionary with the features and their types,
            where types can be specified as either FeatureType enums,
            class instances (NumericalFeature, CategoricalFeature, TextFeature), or strings.
        """
        logger.info("Normalizing Feature Space using FeatureSpaceConverter")
        logger.debug(f"Features specs: {features_specs}")
        fsc = FeatureSpaceConverter()

        # attributing class variables
        self.features_specs = fsc._init_features_specs(features_specs=features_specs)
        logger.debug(f"Features specs normalized: {self.features_specs}")
        self.numeric_features = fsc.numeric_features
        self.categorical_features = fsc.categorical_features
        self.text_features = fsc.text_features
        self.date_features = fsc.date_features

    def _init_stats(self) -> None:
        """Initialize the statistics for the model.

        Note:
            Initializing Data Stats object
            we only need numeric and cat features stats for layers
            crosses and numeric do not need layers init
        """
        if not self.features_stats:
            logger.info("No features stats provided, trying to load local file 🌪️")
            self.stats_instance = DatasetStatistics(
                path_data=self.path_data,
                features_specs=self.features_specs,
                numeric_features=self.numeric_features,
                categorical_features=self.categorical_features,
                text_features=self.text_features,
            )
            self.features_stats = self.stats_instance._load_stats()

    def _add_input_column(self, feature_name: str, dtype) -> None:
        """Add an input column to the model.

        Args:
            feature_name: The name of the feature.
            dtype: Data Type for the feature values.

        """
        logger.debug(f"Adding {feature_name = }, {dtype =} to the input columns")
        self.inputs[feature_name] = tf.keras.Input(
            shape=(1,),
            name=feature_name,
            dtype=dtype,
        )

    def _add_input_signature(self, feature_name: str, dtype) -> None:
        """Add an input signature to the model.

        Args:
            feature_name: The name of the feature.
            dtype: Data Type for the feature values.
        """
        logger.debug(f"Adding {feature_name = }, {dtype =} to the input signature")
        self.signature[feature_name] = tf.TensorSpec(
            shape=(None, 1),
            dtype=dtype,
            name=feature_name,
        )

    def _add_custom_steps(
        self,
        preprocessor: FeaturePreprocessor,
        feature: FeatureType,
        feature_name: str,
    ) -> FeaturePreprocessor:
        """Add custom preprocessing steps to the pipeline.

        Args:
            preprocessor: The preprocessor object.
            feature: The feature object.
            feature_name: The name of the feature.

        Returns:
            FeaturePreprocessor: The preprocessor object with the custom steps added.
        """
        # getting feature object
        _feature = self.features_specs[feature_name]
        for preprocessor_step in feature.preprocessors:
            logger.info(f"Adding custom {preprocessor =} for {feature_name =}, {_feature.kwargs =}")
            preprocessor.add_processing_step(
                layer_class=preprocessor_step,
                name=f"{preprocessor_step.__name__}_{feature_name}",
                **_feature.kwargs,
            )
        return preprocessor

    def _add_pipeline_numeric(self, feature_name: str, input_layer, stats: dict) -> None:
        """Add a numeric preprocessing step to the pipeline.

        Args:
            feature_name (str): The name of the feature to be preprocessed.
            input_layer: The input layer for the feature.
            stats (dict): A dictionary containing the metadata of the feature, including
                the mean and variance of the feature.
        """
        # extracting stats
        mean = stats["mean"]
        variance = stats["var"]

        # getting feature object
        _feature = self.features_specs[feature_name]

        # default output dims for simple transformations
        _out_dims = 1  # FLOAT_NORMALIZED | FLOAT_RESCALED

        # initializing preprocessor
        preprocessor = FeaturePreprocessor(name=feature_name)

        # Check if feature has specific preprocessing steps defined
        if hasattr(_feature, "preprocessors") and _feature.preprocessors:
            logger.info(f"Custom Preprocessors detected 📐: {_feature.preprocessors}")
            self._add_custom_steps(
                preprocessor=preprocessor,
                feature=_feature,
                feature_name=feature_name,
            )

        else:
            # Default behavior if no specific preprocessing is defined
            if _feature.feature_type == FeatureType.FLOAT_NORMALIZED:
                logger.debug("Adding Float Normalized Feature")
                preprocessor.add_processing_step(
                    layer_class="Normalization",
                    mean=mean,
                    variance=variance,
                    name=f"norm_{feature_name}",
                )
            elif _feature.feature_type == FeatureType.FLOAT_RESCALED:
                logger.debug("Adding Float Rescaled Feature")
                rescaling_scale = _feature.kwargs.get("scale", 1.0)  # Default scale is 1.0 if not specified
                preprocessor.add_processing_step(
                    layer_class="Rescaling",
                    scale=rescaling_scale,
                    name=f"rescale_{feature_name}",
                )
            elif _feature.feature_type == FeatureType.FLOAT_DISCRETIZED:
                logger.debug("Adding Float Discretized Feature")
                # output dimentions will be > 1
                _out_dims = len(_feature.kwargs.get("bin_boundaries", 1.0)) + 1
                preprocessor.add_processing_step(
                    layer_class="Discretization",
                    **_feature.kwargs,
                    name=f"discretize_{feature_name}",
                )
                preprocessor.add_processing_step(
                    layer_class="CategoryEncoding",
                    num_tokens=_out_dims,
                    output_mode="one_hot",
                    name=f"one_hot_{feature_name}",
                )
                # for concatenation we need the same format
                # so the cast to float 32 is necessary
                preprocessor.add_processing_step(
                    layer_creator=PreprocessorLayerFactory.cast_to_float32_layer,
                    name=f"cast_to_float_{feature_name}",
                )
            else:
                logger.debug("Adding Float Normalized Feature -> Default Option")
                preprocessor.add_processing_step(
                    layer_class="Normalization",
                    mean=mean,
                    variance=variance,
                    name=f"norm_{feature_name}",
                )
        # defining the pipeline input layer
        _output_pipeline = preprocessor.chain(input_layer=input_layer)

        # defining output
        self.outputs[feature_name] = _output_pipeline

    def _add_pipeline_categorical(self, feature_name: str, input_layer, stats: dict) -> None:
        """Add a categorical preprocessing step to the pipeline.

        Args:
            feature_name (str): The name of the feature to be preprocessed.
            input_layer: The input layer for the feature.
            stats (dict): A dictionary containing the metadata of the feature, including
                the vocabulary of the feature.
        """
        vocab = stats["vocab"]

        # getting feature object
        _feature = self.features_specs[feature_name]

        # initializing preprocessor
        preprocessor = FeaturePreprocessor(name=feature_name)

        # Check if feature has specific preprocessing steps defined
        if hasattr(_feature, "preprocessors") and _feature.preprocessors:
            self._add_custom_steps(
                preprocessor=preprocessor,
                feature=_feature,
                feature_name=feature_name,
            )
        else:
            # Default behavior if no specific preprocessing is defined
            if _feature.feature_type == FeatureType.STRING_CATEGORICAL:
                preprocessor.add_processing_step(
                    layer_class="StringLookup",
                    vocabulary=vocab,
                    num_oov_indices=1,
                    name=f"lookup_{feature_name}",
                )
            elif _feature.feature_type == FeatureType.INTEGER_CATEGORICAL:
                preprocessor.add_processing_step(
                    layer_class="IntegerLookup",
                    vocabulary=vocab,
                    num_oov_indices=1,
                    name=f"lookup_{feature_name}",
                )

        if _feature.category_encoding == CategoryEncodingOptions.EMBEDDING:
            _custom_embedding_size = _feature.kwargs.get("embedding_size")
            _vocab_size = len(vocab) + 1
            logger.debug(f"{_custom_embedding_size = }, {_vocab_size = }")
            emb_size = _custom_embedding_size or _feature._embedding_size_rule(nr_categories=_vocab_size)
            logger.debug(f"{feature_name = }, {emb_size = }")
            preprocessor.add_processing_step(
                layer_class="Embedding",
                input_dim=len(vocab) + 1,
                output_dim=emb_size,
                name=f"embed_{feature_name}",
            )
        elif _feature.category_encoding == CategoryEncodingOptions.ONE_HOT_ENCODING:
            preprocessor.add_processing_step(
                layer_class="CategoryEncoding",
                num_tokens=len(vocab) + 1,
                output_mode="one_hot",
                name=f"one_hot_{feature_name}",
            )
            # for concatenation we need the same format
            # so the cast to float 32 is necessary
            preprocessor.add_processing_step(
                layer_creator=PreprocessorLayerFactory.cast_to_float32_layer,
                name=f"cast_to_float_{feature_name}",
            )

        # we need to flatten the categorical feature
        preprocessor.add_processing_step(
            layer_class="Flatten",
            name=f"flatten_{feature_name}",
        )

        # adding outputs
        self.outputs_categorical[feature_name] = preprocessor.chain(input_layer=input_layer)

    def _add_pipeline_text(self, feature_name: str, input_layer, stats: dict) -> None:
        """Add a text preprocessing step to the pipeline.

        Args:
            feature_name (str): The name of the feature to be preprocessed.
            input_layer: The input layer for the feature.
            stats (dict): A dictionary containing the metadata of the feature, including
        """
        # getting feature object
        _feature = self.features_specs[feature_name]

        # getting stats
        _vocab = stats["vocab"]
        logger.debug(f"TEXT: {_vocab = }")

        # initializing preprocessor
        preprocessor = FeaturePreprocessor(name=feature_name)

        # Check if feature has specific preprocessing steps defined
        if hasattr(_feature, "preprocessors") and _feature.preprocessors:
            self._add_custom_steps(
                preprocessor=preprocessor,
                feature=_feature,
                feature_name=feature_name,
            )
        else:
            # checking if we have stop words provided
            _stop_words = _feature.kwargs.get("stop_words", [])
            if _stop_words:
                preprocessor.add_processing_step(
                    layer_creator=PreprocessorLayerFactory.text_preprocessing_layer,
                    name=f"text_preprocessor_{feature_name}",
                    **_feature.kwargs,
                )
            if "output_sequence_length" not in _feature.kwargs:
                _feature.kwargs["output_sequence_length"] = 35

            # adding text vectorization
            preprocessor.add_processing_step(
                layer_class="TextVectorization",
                name=f"text_vactorizer_{feature_name}",
                vocabulary=_vocab,
                **_feature.kwargs,
            )
            # for concatenation we need the same format
            # so the cast to float 32 is necessary
            preprocessor.add_processing_step(
                layer_creator=PreprocessorLayerFactory.cast_to_float32_layer,
                name=f"cast_to_float_{feature_name}",
            )
        # adding outputs
        self.outputs_categorical[feature_name] = preprocessor.chain(input_layer=input_layer)
        # self.outputs[feature_name] = preprocessor.chain(input_layer=input_layer)

    def _add_pipeline_cross(self) -> None:
        """Add a crossing preprocessing step to the pipeline.

        Args:
            stats (dict): A dictionary containing the metadata of the feature, including
                the list of features it is crossed with and the depth of the crossing.
        """
        for feature_a, feature_b, nr_bins in self.feature_crosses:
            preprocessor = FeaturePreprocessor(name=f"{feature_a}_x_{feature_b}")

            # checking inputs existance for feature A
            for _feature_name in [feature_a, feature_b]:
                # getting feature object
                _feature = self.features_specs[_feature_name]
                _input = self.inputs.get(_feature_name)
                if _input is None:
                    logger.info(f"Creating: {_feature} inputs and signature")
                    _col_dtype = _feature.dtype
                    self._add_input_column(feature_name=_feature, dtype=_col_dtype)

            feature_name = f"{feature_a}_x_{feature_b}"
            preprocessor.add_processing_step(
                layer_class="HashedCrossing",
                num_bins=nr_bins,
                name=f"cross_{feature_name}",
            )
            # for concatenation we need the same format
            # so the cast to float 32 is necessary
            preprocessor.add_processing_step(
                layer_creator=PreprocessorLayerFactory.cast_to_float32_layer,
                name=f"cast_to_float_{feature_name}",
            )
            crossed_input = [self.inputs[feature_a], self.inputs[feature_b]]
            self.outputs[feature_name] = preprocessor.chain(input_layer=crossed_input)

    def _add_pipeline_date(self, feature_name: str, input_layer) -> None:
        """Add a date preprocessing step to the pipeline.

        Args:
            feature_name (str): The name of the feature to be preprocessed.
            input_layer: The input layer for the feature.
        """
        # getting feature object
        _feature = self.features_specs[feature_name]

        # initializing preprocessor
        preprocessor = FeaturePreprocessor(name=feature_name)

        # Check if feature has specific preprocessing steps defined
        if hasattr(_feature, "preprocessors") and _feature.preprocessors:
            logger.info(f"Custom Preprocessors detected 📐: {_feature.preprocessors}")
            self._add_custom_steps(
                preprocessor=preprocessor,
                feature=_feature,
                feature_name=feature_name,
            )
        else:
            # Default behavior if no specific preprocessing is defined
            if _feature.feature_type == FeatureType.DATE:
                logger.debug("Adding Date Parsing layer")
                date_format = _feature.kwargs.get("format", "YYYY-MM-DD")  # Default format if not specified
                preprocessor.add_processing_step(
                    layer_creator=PreprocessorLayerFactory.date_parsing_layer,
                    date_format=date_format,
                    name=f"date_parsing_{feature_name}",
                )

                logger.debug("Adding Date Encoding layer")
                preprocessor.add_processing_step(
                    layer_creator=PreprocessorLayerFactory.date_encoding_layer,
                    name=f"date_encoding_{feature_name}",
                )

                # Optionally, add SeasonLayer
                if _feature.kwargs.get("add_season", False):
                    logger.debug("Adding Season layer")
                    preprocessor.add_processing_step(
                        layer_creator=PreprocessorLayerFactory.date_season_layer,
                        name=f"date_season_{feature_name}",
                    )
            else:
                logger.warning(f"No default preprocessing for {feature_name =} defined")

        # Adding preprocessed layer to the model outputs
        self.outputs[feature_name] = preprocessor.chain(input_layer=input_layer)

    def _prepare_outputs(self) -> None:
        """Preparing the outputs of the model.

        Note:
            Two outputs are possible based on output_model variable.
        """
        logger.info("Building preprocessor Model")
        if self.output_mode == OutputModeOptions.CONCAT:
            self.features_to_concat = list(self.outputs.values()) or []
            self.features_cat_to_concat = list(self.outputs_categorical.values()) or []

            # Reshape tensors to make them compatible
            reshaped_features = []
            for feature in self.features_to_concat:
                reshaped = tf.keras.layers.Reshape((-1,))(feature) if len(feature.shape) == 2 | 4 else feature
                reshaped_features.append(reshaped)

            # Concatenate numerical features
            if reshaped_features:
                concat_num = tf.keras.layers.Concatenate(
                    name="ConcatenateNumeric",
                    axis=-1,
                )(reshaped_features)
            else:
                concat_num = None

            # Concatenate categorical features
            if self.features_cat_to_concat:
                concat_cat = tf.keras.layers.Concatenate(
                    name="ConcatenateCategorical",
                    axis=-1,
                )(self.features_cat_to_concat)
            else:
                concat_cat = None

            # Combine numerical and categorical features
            if concat_num is not None and concat_cat is not None:
                self.concat_all = tf.keras.layers.Concatenate(
                    name="ConcatenateAll",
                    axis=-1,
                )([concat_num, concat_cat])
            elif concat_num is not None:
                self.concat_all = concat_num
            elif concat_cat is not None:
                self.concat_all = concat_cat
            else:
                self.concat_all = None

            # Adding transformer layers
            if self.transfo_nr_blocks and self.transfo_placement == TransformerBlockPlacementOptions.CATEGORICAL:
                logger.info(f"Adding transformer blocks CATEGORICAL: #{self.transfo_nr_blocks}")
                for block_idx in range(self.transfo_nr_blocks):
                    self.concat_all = PreprocessorLayerFactory.transformer_block_layer(
                        dim_model=self.concat_all.shape[1],
                        num_heads=self.transfo_nr_heads,
                        ff_units=self.transfo_ff_units,
                        dropout_rate=self.transfo_dropout_rate,
                        name=f"transformer_block_{block_idx}_{self.transfo_nr_heads}heads",
                    )(self.concat_all)

            if self.transfo_nr_blocks and self.transfo_placement == TransformerBlockPlacementOptions.ALL_FEATURES:
                _transfor_input_shape = self.concat_all.shape[1]
                logger.info(
                    f"Adding transformer blocks ALL_FEATURES: #{self.transfo_nr_blocks}",
                )
                for block_idx in range(self.transfo_nr_blocks):
                    self.concat_all = PreprocessorLayerFactory.transformer_block_layer(
                        dim_model=_transfor_input_shape,
                        num_heads=self.transfo_nr_heads,
                        ff_units=self.transfo_ff_units,
                        dropout_rate=self.transfo_dropout_rate,
                        name=f"transformer_block_{block_idx}_{self.transfo_nr_heads}heads",
                    )(self.concat_all)

            logger.info("Concatenating outputs mode enabled")
        else:
            outputs = OrderedDict([(k, None) for k in self.inputs if k in self.outputs])
            outputs.update(OrderedDict(self.outputs))
            self.outputs = outputs
            logger.info("OrderedDict outputs mode enabled")

    def build_preprocessor(self) -> tf.keras.Model:
        """Building preprocessing model.

        Returns:
            tf.keras.Model: The preprocessing model.
        """
        # preparing statistics if they do not exist
        if not self.features_stats or self.overwrite_stats:
            logger.info("No input features_stats detected !")
            self.features_stats = self.stats_instance.main()
            logger.debug(f"Features Stats were calculated: {self.features_stats}")

        # NUMERICAL AND CATEGORICAL FEATURES (based on stats)
        for _key in self.features_stats:
            logger.info(f"Processing feature type: {_key = }")
            for feature_name, stats in self.features_stats[_key].items():
                logger.info(f"Found {stats =}")
                dtype = stats.get("dtype")
                logger.info(f"Processing {feature_name = }, {dtype = } 📊")
                # adding inputs
                self._add_input_column(feature_name=feature_name, dtype=dtype)
                self._add_input_signature(feature_name=feature_name, dtype=dtype)
                input_layer = self.inputs[feature_name]

                # NUMERIC FEATURES
                if "mean" in stats:
                    self._add_pipeline_numeric(
                        feature_name=feature_name,
                        input_layer=input_layer,
                        stats=stats,
                    )
                # CATEGORICAL FEATURES
                elif "vocab" in stats and feature_name not in self.text_features:
                    self._add_pipeline_categorical(
                        feature_name=feature_name,
                        input_layer=input_layer,
                        stats=stats,
                    )
        # CROSSING FEATURES (based on defined inputs)
        if self.feature_crosses:
            logger.info("Processing feature type: cross feature")
            self._add_pipeline_cross()

        # TEXT FEATURES (based on defined inputs)
        for feature_name in self.text_features:
            logger.info(f"Processing feature type (text): {feature_name}")
            self._add_input_column(feature_name=feature_name, dtype=tf.string)
            self._add_input_signature(feature_name=feature_name, dtype=tf.string)
            input_layer = self.inputs[feature_name]
            self._add_pipeline_text(
                feature_name=feature_name,
                input_layer=input_layer,
                stats=stats,
            )

        # DATE FEATURES
        for feat_name in self.date_features:
            logger.info(f"Processing feature type (date): {feat_name}")
            self._add_input_column(feature_name=feat_name, dtype=tf.string)
            self._add_input_signature(feature_name=feat_name, dtype=tf.string)
            input_layer = self.inputs[feat_name]
            self._add_pipeline_date(
                feature_name=feat_name,
                input_layer=input_layer,
                # stats=stats,
            )

        # Preparing outputs
        logger.info("Preparing outputs for the model")
        self._prepare_outputs()

        # building model
        logger.info("Building preprocessor Model 🏗️")
        self.model = tf.keras.Model(
            inputs=self.inputs,
            outputs=self.concat_all,
            name="preprocessor",
        )

        # displaying information.
        logger.info("Building preprocessor Model")
        _output_dims = (
            self.model.output_shape[1] if self.output_mode == OutputModeOptions.CONCAT else self.model.output_shape
        )

        logger.info(f"Preprocessor Model built successfully ✅, summary: {self.model.summary()}")
        logger.info(f"Imputs: {self.inputs.keys()}")
        logger.info(f"Output model mode: {self.output_mode} with size: {_output_dims}")
        return {
            "model": self.model,
            "inputs": self.inputs,
            "signature": self.signature,
            "output_dims": _output_dims,
        }

    def batch_predict(self, data: tf.data.Dataset, model: tf.keras.Model = None) -> Generator:
        """Helper function for batch prediction on DataSets.

        Args:
            data (tf.data.Dataset): Data to be used for batch predictions.
            model (tf.keras.Model): Model to be used for batch predictions.
        """
        logger.info("Batch predicting the dataset")
        _model = model or self.model
        for batch in data:
            yield _model.predict(batch)

    def save_model(self, model_path: str) -> None:
        """Saving model locally.

        Args:
            model_path (str): Path to the model to be saved.
        """
        logger.info(f"Saving model to: {model_path}")
        self.model.save(model_path)
        logger.info("Model saved successfully")

    def plot_model(self, filename: str = "Model_Architecture.png") -> None:
        """Plotting model architecture.

        Args:
            filename (str): The name of the file to save the plot to.

        Note:
            This function requires graphviz to be installed on the system
            and pydot library (dependency in the dev group).
        """
        logger.info("Plotting model")
        return tf.keras.utils.plot_model(
            self.model,
            to_file=filename,
            show_shapes=True,
            show_dtype=True,
            show_layer_names=True,
            show_trainable=True,
            dpi=100,
            # rankdir="LR",
        )
