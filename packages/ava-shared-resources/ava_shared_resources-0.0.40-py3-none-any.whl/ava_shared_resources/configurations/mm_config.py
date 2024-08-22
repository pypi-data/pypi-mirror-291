"""Configuration models for artifacts.

Module contains configuration models for artifacts that are used in the model manager service and preprocessor service.
"""
from pathlib import Path
from typing import List, Dict, Union, Optional, Tuple

from pydantic import BaseModel, Field, field_validator, conint
from pydantic_settings import BaseSettings
from typing_extensions import Annotated

from ava_shared_resources.config_processing_utils import merge_configs
from ava_shared_resources.configurations.config import ClientConfig
from ava_shared_resources.data_io_utils import load_toml


class W2VModelParamsModel(BaseModel):
    """W2V model parameters.

    Contains parameters for w2v model. If version is None then w2v model is not applied at the pipeline.
    """

    w2v_model_version: Optional[int] = None
    w2v_model_type: Optional[str] = None
    n_gram_length: Optional[List[int]] = None
    model_name: Annotated[Optional[str], Field(validate_default=True)] = None

    @field_validator("model_name", mode="before")
    def set_model_name(cls, value, values):
        """Setter of model's name.

        Sets the w2v model name configuration based on the other w2v parameters
        :params value: value for `model_name` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: model name
        """
        w2v_model_type = values.data.get("w2v_model_type")

        if w2v_model_type is None:
            return None
        return (
            f"w2v_{w2v_model_type}_dict.onnxruntime"
            if w2v_model_type == "fused"
            else "w2v_dict.onnxruntime"
        )


class PreprocessorParamsModel(BaseModel):
    """Preprocessor parameters.

    Contains parameters for preprocessor service related the client. If version of normalizer is None then normalizer
    is not applied at the pipeline. If tokenizer class is None the tokenizer is not applied at the pipeline.
    """

    normalizer_version: Optional[int] = None
    tokenizer_class: Optional[str] = None
    chunking_tokenizer: Optional[str] = None


class ArticleSearchRegistryModel(BaseModel):
    """Article Search registry model.

    Contains parameters for initialization ArticleSearchRegistry
    """

    model_type: str
    model_version: int
    s2v_models: List[str]
    max_seq_len: Optional[int] = None
    batch_size: int = 10
    to_vectorize_query_models: List[str]
    models_mapping: Dict[str, str]
    content_id_field: str
    content_role_field: str
    to_enrich_query: Annotated[int, Field(validate_default=True)] = 0
    normalize_annotations_flag: bool
    annotations_field: Optional[str] = None
    annotations_label_field: Optional[str] = None
    combine_normalized_fields_flag: bool
    combine_normalized_field: Optional[str] = None
    to_normalize_vector: bool
    w2v_model_params: W2VModelParamsModel = W2VModelParamsModel()
    preprocessor_params: PreprocessorParamsModel = PreprocessorParamsModel()
    model_names: Annotated[Optional[Dict[str, str]], Field(validate_default=True)] = None
    field_names: Annotated[Optional[List[str]], Field(validate_default=True)] = None

    @field_validator("model_names", mode="before")
    def set_model_names(cls, value, values):
        """Setter of models' name.

        Sets the s2v model's name configuration based on the other ArticleSearchRegistry parameters
        :params value: value for `model_names` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: list of models' name
        """
        model_type = values.data.get("model_type")
        w2v_model_params = values.data.get("w2v_model_params")
        s2v_models = values.data.get("s2v_models")
        if model_type == "sif_s2v":
            if w2v_model_params.w2v_model_type == "plain":
                return {
                    s2v_model: f"{s2v_model}_vecs.onnxruntime"
                    for s2v_model in s2v_models
                }
            else:
                return {
                    s2v_model: f"{s2v_model}_{w2v_model_params.w2v_model_type}_vecs.onnxruntime"
                    for s2v_model in s2v_models
                }
        else:
            return {s2v_model: f"{s2v_model}.onnxruntime" for s2v_model in s2v_models}

    @field_validator("field_names", mode="before")
    def set_field_names(cls, value, values):
        """Setter of fields' names.

        Sets the fields list to configuration based on the models_mapping ArticleSearchRegistry parameter
        :params value: value for `field_names` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: list of fields' names
        """
        models_mapping = values.data.get("models_mapping")
        return list(models_mapping.keys())

    @field_validator("to_enrich_query", mode="before")
    def set_to_enrich_query(cls, value, values):
        """Setter of to_enrich_query. The 'to_enrich_query' parameter is used for duplication of user query.

        Sets the to_enrich_query to configuration based on the to_vectorize_query_models and models_mapping
        ArticleSearchRegistry parameters
        :params value: value for `to_enrich_query` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: to_enrich_query value
        """
        models_mapping = values.data.get("models_mapping")
        to_vectorize_query_models = values.data.get("to_vectorize_query_models")

        # duplication_count determines the no. of times we need to duplicate the user query
        duplication_count = len(list(models_mapping.keys())) - len(
            to_vectorize_query_models
        )

        if duplication_count == 0:
            return 0
        elif len(to_vectorize_query_models) == 1:
            return duplication_count
        else:
            raise ValueError(
                f"The number of models used for vectorizing content: {len(models_mapping.keys())} and "
                f"user query: {len(to_vectorize_query_models)} doesn't match. "
                f"The Number of models should either match or only one model should be used for "
                f"vectorizing user query."
            )


class IntentDetectionRegistryModel(BaseModel):
    """Intent Detection registry model.

    Contains parameters for initialization IntentDetectionRegistry
    """

    intent_type: str = "generic"
    model_type: str = "lstm_classifier"
    model_version: int
    max_seq_len: int = 32
    number_classes: int
    is_intent_lookup: bool = False
    w2v_model_params: W2VModelParamsModel = W2VModelParamsModel()
    preprocessor_params: PreprocessorParamsModel = PreprocessorParamsModel()
    model_name: Annotated[Optional[str], Field(validate_default=True)] = None

    @field_validator("model_name", mode="before")
    def set_model_name(cls, value, values):
        """Setter of model's name.

        Sets the intent detection model name configuration based on the other IntentDetectionRegistry params
        :params value: value for `model_name` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: model name
        """
        intent_type = values.data.get("intent_type")

        return f"{intent_type}_id.onnxruntime"


class ClientConfigModel(BaseModel):
    """Client configuration model.

    Client configuration model, that used for building specific article search and intent detection flows
    """

    article_search_registry: Optional[ArticleSearchRegistryModel] = None
    intent_detection_registries: Optional[List[IntentDetectionRegistryModel]] = None
    intent_types: Annotated[Optional[List[str]], Field(validate_default=True)] = None

    @field_validator("intent_types", mode="before")
    def set_intent_types(cls, value, values):
        """Setter of intents types.

        Sets the list supported intents types for detection
        :params value: value for `intent_types` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: model name
        """
        intent_detection_registries = values.data.get("intent_detection_registries")

        if intent_detection_registries:
            return [
                intent_detection_registry.intent_type
                for intent_detection_registry in intent_detection_registries
            ]


class TritonInputsSTModel(BaseModel):
    """Model for Sentence Transformers onnx model's Inputs.

    Builds the inputs for Sentence Transformers onnx model's that used for Triton Server
    """

    input_data: Dict[str, List[List[Optional[int]]]]
    data_types: Tuple[str, str] = ("int64", "INT64")
    output_name: str = "embedding"


class TritonInputW2VModel(BaseModel):
    """Model for W2V onnx model's Inputs.

    Builds the inputs for W2V onnx model's that used for Triton Server
    """

    n_gram_length: Optional[List[int]] = None
    input_data: Dict[str, Union[List[List[int]], List[List[List[int]]]]]
    input_length: Optional[Dict[str, List[List[conint(ge=0)]]]] = None
    data_types: Tuple[str, str] = ("int32", "INT32")
    length_types: Tuple[str, str] = ("float32", "FP32")
    output_name: str = "concatenate"


class TritonInputIDModel(BaseModel):
    """Model for Intent Detection onnx model's Inputs.

    Builds the inputs for Intent Detection onnx model's that used for Triton Server
    """

    input_embedding: Optional[Dict[str, List[List[List[float]]]]] = None
    input_length: Dict[str, List[List[conint(ge=0)]]]
    length_types: Tuple[str, str] = ("int32", "INT32")
    embedding_types: Tuple[str, str] = ("float32", "FP32")
    output_name: str = "output_probabilities"


class TritonInputS2VModel(BaseModel):
    """Model for sif S2V onnx model's Inputs.

    Builds the inputs for sif S2V onnx model's that used for Triton Server
    """

    input_data: Dict[str, List[List[int]]]
    input_embedding: Optional[Dict[str, List[List[List[float]]]]] = None
    input_length: Dict[str, List[List[conint(ge=0)]]]
    length_types: Tuple[str, str] = ("int32", "INT32")
    data_types: Tuple[str, str] = ("int32", "INT32")
    embedding_types: Tuple[str, str] = ("float32", "FP32")
    output_name: str = "embedding"


class APPSettings(BaseSettings):
    """Base setting of the AVA Model Manager.

    Class creates the application config. Also contains default values
    """

    app_name: str
    env: str = "prd"
    artifacts_path: str
    config_path: str
    deployment: str
    clients_list: Annotated[Optional[List[ClientConfig]], Field(validate_default=True)] = None
    model_manager_workers: int = 1
    clients_config: Annotated[Optional[Dict[ClientConfig, ClientConfigModel]], Field(validate_default=True)] = None

    @field_validator("clients_list", mode="before")
    def set_clients_list(cls, value, values):
        """Setter of clients' list.

        Sets the classification configuration based on the clients list and the environment
        :params value: value for `clients_config` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: list of Clients
        """
        env = values.data.get("env")
        deployment = values.data.get("deployment")
        app_name = values.data.get("app_name")
        config_path = values.data.get("config_path")

        if deployment is None:
            if app_name == "preprocessor":
                return None
            else:
                raise ValueError("Deployment should be identified for every deployment")

        try:
            base_config = load_toml(Path(f"{config_path}{deployment}/config.toml"))
            env_config = load_toml(Path(f"{config_path}{deployment}/config_{env}.toml"))
            merged_config = merge_configs(base_config, env_config)
            return [
                ClientConfig(deployment=deployment, **client)
                for client in merged_config["clients"]
            ]

        except Exception as e:
            raise ValueError(
                f"Check please that you have correct configuration for deployment {deployment}: {e}"
            )

    @field_validator("clients_config", mode="before")
    def set_clients_config(cls, value, values):
        """Setter of clients' configuration.

        Sets the classification configuration based on the clients list and the environment
        :params value: value for `clients_config` that is set during the class initialization
        :params values: values that are set during the class initialization
        :return: dictionary with Client as key and Client's configuration as value
        """
        env = values.data.get("env")
        clients_list = values.data.get("clients_list")
        app_name = values.data.get("app_name")
        config_path = values.data.get("config_path")

        if not clients_list:
            if app_name == "preprocessor":
                return None
            else:
                raise ValueError("Clients list cannot be empty")

        clients_config = dict()
        try:
            for client in clients_list:
                base_config = load_toml(
                    Path(
                        f"{config_path}{client.deployment}/{client.business_unit}/{client.language}/config.toml"
                    )
                )
                env_config = load_toml(
                    Path(
                        f"{config_path}{client.deployment}/{client.business_unit}/{client.language}/config_{env}.toml"
                    )
                )
                merged_config = merge_configs(base_config, env_config)
                client_article_search_registry = ArticleSearchRegistryModel(
                    **merged_config["article_search_registry"]
                )
                intent_detection_registries = merged_config[
                    "intent_detection_registries"
                ]

                client_intent_detection_registries = [
                    IntentDetectionRegistryModel(
                        intent_type=intent_type,
                        **intent_detection_registries[intent_type],
                    )
                    for intent_type in intent_detection_registries
                ]

                clients_config[client] = ClientConfigModel(
                    article_search_registry=client_article_search_registry,
                    intent_detection_registries=client_intent_detection_registries,
                )

            return clients_config

        except KeyError as e:
            raise ValueError(
                f"Check that all clients have configuration. Configuration for client `{e}` does not present"
            )
