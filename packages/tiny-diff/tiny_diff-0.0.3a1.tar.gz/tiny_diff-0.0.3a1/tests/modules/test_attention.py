import pytest
from tiny_diff.modules.attention import (
    CausalVisualAttention,
    VisualAttention,
)
from torch import Tensor, randn

from tests.conftest import CONTEXT_DIM, B, C, H, W


@pytest.fixture()
def q() -> Tensor:
    """Query tensor."""
    return randn(B, C, H, W)


@pytest.fixture()
def k() -> Tensor:
    """Key tensor."""
    return randn(B, C, H * 2, W * 2)


@pytest.fixture()
def v() -> Tensor:
    """Value tensor."""
    return randn(B, C, H * 2, W * 2)


@pytest.fixture()
def va_layer() -> VisualAttention:
    """Visual attention layer."""
    return VisualAttention(channels=C, embed_dim=32, num_heads=8)


@pytest.fixture()
def cva_layer() -> CausalVisualAttention:
    """Conditional Visual Attention layer."""
    return CausalVisualAttention(
        channels=C, context_dim=CONTEXT_DIM, embed_dim=32, num_heads=8
    )


def test_visual_attention(q: Tensor, k: Tensor, v: Tensor, va_layer: VisualAttention):
    """Tests that the output shape matches."""
    result = va_layer(q, k, v)

    assert va_layer.batch_first
    assert result.shape == q.shape


def test_causal_visual_attention(
    q: Tensor, attention_context, cva_layer: VisualAttention
):
    """Tests that the output shape matches."""
    result = cva_layer(q, attention_context)
    assert result.shape == q.shape
