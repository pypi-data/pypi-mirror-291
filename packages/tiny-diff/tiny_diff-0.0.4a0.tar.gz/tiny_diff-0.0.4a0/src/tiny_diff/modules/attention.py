from typing import Optional

from torch import Tensor, nn
from typing_extensions import override


class CSA(nn.Module):
    """Pure Convolutional Self attention.

    Tensors are assumed to be in BxCxHxW format

    Args:
        channels: input channels
        height: input tensor height
        width: input tensor width
        kernel_size: kernel size to use. Defaults to 5.

    See Also:
        https://developer.nvidia.com/blog/emulating-the-attention-mechanism-in-transformer-models-with-a-fully-convolutional-network/
    """

    def __init__(
        self,
        channels: int,
        height: int = None,
        width: int = None,
        input_shape: int = None,
        kernel_size: int = 5,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.channels = channels
        self.height = height or input_shape
        self.width = width or input_shape
        self.kernel_size = kernel_size

        self.dw_conv = nn.Conv2d(
            in_channels=channels,
            out_channels=channels,
            groups=channels,
            kernel_size=kernel_size,
            padding="same",
        )

        self.pw_conv = nn.ModuleDict()
        self.pw_conv["Q"] = nn.Conv2d(
            in_channels=channels,
            out_channels=height * width,
            kernel_size=1,
            padding="same",
        )
        self.pw_conv["QK"] = nn.Conv2d(
            in_channels=height * width,
            out_channels=channels,
            kernel_size=1,
            padding="same",
        )
        self.pw_conv["QKV"] = nn.Sequential(
            nn.Conv2d(
                in_channels=channels,
                out_channels=3 * channels,
                kernel_size=1,
                padding="same",
            ),
            nn.Conv2d(
                in_channels=3 * channels,
                out_channels=channels,
                kernel_size=1,
                padding="same",
            ),
        )

        self.sigmoid = nn.Sigmoid()

    @staticmethod
    def hadamard(A: Tensor, B: Tensor) -> Tensor:
        """Performs hadamard product."""
        return A * B

    @override
    def forward(self, x: Tensor, e: Tensor = None):
        B, C, H, W = x.shape
        HW = H * W

        V = self.dw_conv(x)
        Q = self.pw_conv["Q"](V)

        K = Q.view(B, HW, HW)
        K = K.mT.reshape(B, HW, H, W)

        QK = self.hadamard(Q, K)
        QK = self.pw_conv["QK"](QK)
        QK = self.sigmoid(QK)

        QKV = self.hadamard(V, QK)
        return self.pw_conv["QKV"](QKV)


class VisualAttention(nn.MultiheadAttention):
    """Multihead attention for visual transformers."""

    def __init__(
        self,
        channels: int,
        embed_dim: Optional[int] = None,
        head_dim: int = 64,
        batch_first: bool = True,
        num_heads: int = 8,
        proy_bias: bool = False,
        **kwargs,
    ) -> None:
        self.channels = channels
        self.proy_bias = proy_bias
        embed_dim = embed_dim or num_heads * head_dim
        super().__init__(
            embed_dim=embed_dim, batch_first=batch_first, num_heads=num_heads, **kwargs
        )
        self.proj = nn.ModuleDict()

        self.proj["q"] = self._get_q_proy()
        self.proj["k"] = self._get_k_proy()
        self.proj["v"] = self._get_v_proy()

        self.result_proj = nn.Linear(embed_dim, channels)

    def _get_proy(
        self,
        in_features: Optional[int] = None,
        out_features: Optional[int] = None,
        bias: bool = False,
        **kwargs,
    ) -> nn.Module:
        in_features = in_features or self.channels
        out_features = out_features or self.embed_dim
        bias = bias or self.proy_bias
        return nn.Linear(
            in_features=in_features,
            out_features=out_features,
            bias=bias,
            **kwargs,
        )

    def _get_q_proy(self) -> nn.Module:
        return self._get_proy()

    def _get_k_proy(self) -> nn.Module:
        return self._get_proy()

    def _get_v_proy(self) -> nn.Module:
        return self._get_proy()

    @staticmethod
    def _reshape(x: Tensor, b: int, c: int):
        return x.view(b, -1, c)

    @staticmethod
    def _q_reshape(q, *args, **kwargs):
        return VisualAttention._reshape(q, *args, **kwargs)

    @staticmethod
    def _k_reshape(k, *args, **kwargs):
        return VisualAttention._reshape(k, *args, **kwargs)

    @staticmethod
    def _v_reshape(v, *args, **kwargs):
        return VisualAttention._reshape(v, *args, **kwargs)

    @override
    def forward(
        self, query: Tensor, key: Tensor, value: Tensor, **kwargs
    ) -> tuple[Tensor, Optional[Tensor]]:
        B, C, H, W = query.shape
        q = self._q_reshape(query, B, C)
        k = self._k_reshape(key, B, C)
        v = self._v_reshape(value, B, C)

        q = self.proj["q"](q)
        k = self.proj["k"](k)
        v = self.proj["v"](v)

        result, _ = super().forward(q, k, v, **kwargs)
        result = self.result_proj(result)
        return result.view(B, C, H, W)


class SelfVisualAttention(VisualAttention):
    """Self Visual attention."""

    @override
    def forward(self, query: Tensor, **kwargs) -> tuple[Tensor, Optional[Tensor]]:
        key = value = query
        return super().forward(query, key, value, **kwargs)


class CausalVisualAttention(VisualAttention):
    """Causal Visual Attention."""

    def __init__(self, context_dim: int, **kwargs) -> None:
        self.context_dim = context_dim
        super().__init__(**kwargs)

    def _get_k_proy(self) -> nn.Module:
        return self._get_proy(in_features=self.context_dim)

    def _get_v_proy(self) -> nn.Module:
        return self._get_proy(in_features=self.context_dim)

    @override
    @staticmethod
    def _k_reshape(k, *args, **kwargs):
        """No need to reshape as it should already be embedded/flattened."""
        return k

    @staticmethod
    def _v_reshape(v, *args, **kwargs):
        return v

    @override
    def forward(
        self, query: Tensor, context: Tensor, **kwargs
    ) -> tuple[Tensor, Optional[Tensor]]:
        key = value = context
        return super().forward(query, key, value, **kwargs)
