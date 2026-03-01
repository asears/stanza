from __future__ import annotations

from dataclasses import dataclass

# TODO: perhaps put the enums in this file
from stanza.models.classifiers.utils import WVType, ExtraVectors, ModelType

@dataclass
class CNNConfig:  # pylint: disable=too-many-instance-attributes, too-few-public-methods
        filter_channels: int | tuple[int, ...]
        filter_sizes: tuple[int | tuple[int, int], ...]
        fc_shapes: tuple[int, ...]
        dropout: float
        num_classes: int
        wordvec_type: WVType
        extra_wordvec_method: ExtraVectors
        extra_wordvec_dim: int
        extra_wordvec_max_norm: float
        char_lowercase: bool
        charlm_projection: int | None
        has_charlm_forward: bool
        has_charlm_backward: bool

        use_elmo: bool
        elmo_projection: int | None

        bert_model: str | None
        bert_finetune: bool
        bert_hidden_layers: int | None
        force_bert_saved: bool

        use_peft: bool
        lora_rank: int | None
        lora_alpha: float | None
        lora_dropout: float | None
        lora_modules_to_save: list[str] | None
        lora_target_modules: list[str] | None

        bilstm: bool
        bilstm_hidden_dim: int
        maxpool_width: int
        model_type: ModelType

@dataclass
class ConstituencyConfig:  # pylint: disable=too-many-instance-attributes, too-few-public-methods
        fc_shapes: tuple[int, ...]
        dropout: float
        num_classes: int

        constituency_backprop: bool
        constituency_batch_norm: bool
        constituency_node_attn: bool
        constituency_top_layer: bool
        constituency_all_words: bool

        model_type: ModelType
