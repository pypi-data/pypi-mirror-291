from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, Union

import torch
from diffusers.models.attention import Attention
from torch import nn
from typing_extensions import override

from tiny_diff.utils import match_shape

from .attention import CSA
from .conv import PreNormActConvBlock
from .resampling import Downsample, Interpolation, Upsample


class ResidualBlock(nn.Module):
    """Block for residual layers.

    See Also:
        https://arxiv.org/pdf/2302.06112.pdf.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        drop_p: float = None,
        zero_init: bool = False,
        **kwargs,
    ):
        super().__init__()
        self.conv1 = PreNormActConvBlock(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            attention=False,
            drop_p=None,
            zero_init=False,
            **kwargs,
        )
        self.conv2 = PreNormActConvBlock(
            in_channels=out_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            attention=False,
            drop_p=drop_p,
            zero_init=zero_init,
            **kwargs,
        )
        # TODO: zero init might affect VAE

        self.shortcut = nn.Identity()
        if in_channels != out_channels:
            self.shortcut = nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=1,
                stride=1,
                padding="same",
            )

    @override
    def forward(self, x):
        h = self.conv1(x)
        h = self.conv2(h)
        h = h + self.shortcut(x)
        return h


class EmbeddingsResidualBlock(ResidualBlock):
    """Block for residual layer with embeddings."""

    def __init__(
        self,
        embed_channels: int,
        out_channels: int,
        nonlinearity: Optional[nn.Module] = None,
        **kwargs,
    ):
        super().__init__(out_channels=out_channels, nonlinearity=nonlinearity, **kwargs)

        proy_layers = [nn.Linear(embed_channels, out_channels)]
        if nonlinearity:
            proy_layers = [deepcopy(nonlinearity), *proy_layers]
        self.proy_emb = nn.Sequential(*proy_layers)

    @override
    def forward(self, x: torch.Tensor, e: torch.Tensor):
        h = self.conv1(x)

        e = self.proy_emb(e)
        e = match_shape(e, like=h)

        h = h + e
        h = self.conv2(h)
        h = h + self.shortcut(x)
        return h


class RABlock(nn.Module):
    """Residual block with attention at the end."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        height: Optional[int] = None,
        width: Optional[int] = None,
        input_shape: Optional[int] = None,
        attention_head_dim: int = 8,
        num_groups: Optional[int] = None,
        **kwargs,
    ):
        super().__init__()
        height = height or input_shape
        width = width or input_shape
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.r1 = EmbeddingsResidualBlock(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            num_groups=num_groups,
            **kwargs,
        )
        if num_groups < 0:
            num_groups = out_channels // (-num_groups)
        self.a = Attention(
            out_channels,
            heads=out_channels // attention_head_dim,
            dim_head=attention_head_dim,
            rescale_output_factor=1,
            norm_num_groups=num_groups,
            spatial_norm_dim=None,
            residual_connection=True,
            bias=True,
            upcast_softmax=True,
            _from_deprecated_attn_block=True,
        )

    @override
    def forward(self, x, e):
        h = self.r1(x, e)
        h = self.a(h)
        return h


class RARBlock(RABlock):
    """Residual layer with attention in the middle."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        **kwargs,
    ):
        super().__init__(in_channels=in_channels, out_channels=out_channels, **kwargs)
        self.r2 = EmbeddingsResidualBlock(
            in_channels=self.out_channels,
            out_channels=self.out_channels,
            **kwargs,
        )

    @override
    def forward(self, x: torch.Tensor, e: torch.Tensor):
        h = super().forward(x, e)
        h = self.r2(h, e)
        return h


class ResidualLayerABC(nn.Module, ABC):
    """Residual layer abstract class.

    Args:
        in_channels: input's channel dim size
        out_channels: output's channel dim size
        n_blocks: number of blocks to use.
        attention: whether to include attention or not.
        input_shape: input's height and width dimension.
    """

    @property
    @abstractmethod
    def residual_block_cls(self):
        """Class to use in residual conv blocks."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        n_blocks: int = 2,
        attention: bool = False,
        input_shape: Optional[int] = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.n_blocks = n_blocks
        self.blocks = nn.ModuleList()
        self.attention = attention
        self.input_shape = input_shape
        self.res_kwargs = kwargs
        self._setup_blocks()

    def _setup_blocks(self, **kwargs):
        self.blocks.append(
            self.residual_block_cls(
                in_channels=self.in_channels,
                out_channels=self.out_channels,
                scale_factor=None,
                **self.res_kwargs,
                **kwargs,
            )
        )
        if self.attention:
            self.blocks.append(self._get_attention())
        for _ in range(1, self.n_blocks):
            self.blocks.append(
                self.residual_block_cls(
                    in_channels=self.out_channels,
                    out_channels=self.out_channels,
                    scale_factor=None,
                    **self.res_kwargs,
                    **kwargs,
                )
            )
            if self.attention:
                self.blocks.append(self._get_attention())

    def _get_attention(self):
        return CSA(
            channels=self.out_channels,
            height=self.input_shape,
            width=self.input_shape,
        )

    def residual_forward(self, h: torch.Tensor, *args, **kwargs):
        """Residual blocks forward."""
        for block in self.blocks:
            h = block(h, *args, **kwargs)
        return h

    @override
    def forward(self, x: torch.Tensor, *args, **kwargs):
        return self.residual_forward(x, *args, **kwargs)

    @property
    def last_layer(self) -> nn.Module:
        """Last block of the residual layer."""
        return self.blocks[-1]


class ResizeResidualLayerABC(ResidualLayerABC):
    """Residual layer that performs resizing."""

    @property
    @abstractmethod
    def residual_block_cls(self):
        """Class to use in the residual blocks."""

    def __init__(self, scale_factor: float, **kwargs):
        self.scale_factor = scale_factor
        super().__init__(**kwargs)
        self.resize = self._get_resize_layer()

    @abstractmethod
    def _get_resize_layer(self) -> nn.Module: ...

    @override
    def forward(self, *args, **kwargs):
        h = super().forward(*args, **kwargs)
        h = self.resize(h)
        return h


class InterpolationResidualLayerABC(ResizeResidualLayerABC):
    """Residual layer with interpolation resizing."""

    @property
    @abstractmethod
    def resize_cls(self) -> type[Interpolation]:
        """Class used in resizing layers."""

    def __init__(self, interpolation_mode: str = "bilinear", **kwargs):
        self.interpolation_mode = interpolation_mode
        super().__init__(**kwargs)

    def _get_resize_layer(self) -> nn.Module:
        return self.resize_cls(
            scale_factor=self.scale_factor, mode=self.interpolation_mode
        )


class ConvResizeResidualLayerABC(ResizeResidualLayerABC):
    """Residual layer with convolutional resizing."""

    @property
    @abstractmethod
    def conv_cls(self) -> type[Union[nn.Conv2d, nn.ConvTranspose2d]]:
        """Class to use in convolution layers."""

    def __init__(self, kernel_size: int, **kwargs):
        self.kernel_size = kernel_size
        super().__init__(kernel_size=kernel_size, **kwargs)

    @property
    def padding(self):
        """Padding to use in convolutions."""
        return 1

    def _get_resize_layer(self, **kwargs) -> nn.Module:
        return self.conv_cls(
            self.out_channels,
            self.out_channels,
            kernel_size=self.kernel_size,
            stride=int(self.scale_factor),
            padding=self.padding,
            **kwargs,
        )


class ResidualLayer(ResidualLayerABC):
    """Residual layer."""

    residual_block_cls = ResidualBlock


class EResidualLayer(ResidualLayerABC):
    """Residual layer with embeddings."""

    residual_block_cls = EmbeddingsResidualBlock


class DownsampleResidualLayer(InterpolationResidualLayerABC):
    """Residual layer with interpolation downscaling."""

    residual_block_cls = ResidualBlock
    resize_cls = Downsample


class UpsampleResidualLayer(InterpolationResidualLayerABC):
    """Residual layer with interpolation upscaling."""

    residual_block_cls = ResidualBlock
    resize_cls = Upsample


class DownsampleEResidualLayer(InterpolationResidualLayerABC):
    """Residual layer with embeddings and interpolation downscaling."""

    residual_block_cls = EmbeddingsResidualBlock
    resize_cls = Downsample


class UpsampleEResidualLayer(InterpolationResidualLayerABC):
    """Residual layer with embeddings and interpolation upscaling."""

    residual_block_cls = EmbeddingsResidualBlock
    resize_cls = Upsample


class ConvResidualLayer(ConvResizeResidualLayerABC):
    """Residual layer with convolutions for downscaling."""

    residual_block_cls = ResidualBlock
    resize_cls = nn.Conv2d


class TransConvResidualLayer(ConvResizeResidualLayerABC):
    """Residual layer with transposed convolutions for upscaling."""

    residual_block_cls = ResidualBlock
    resize_cls = nn.ConvTranspose2d


class ConvEResidualLayer(ConvResizeResidualLayerABC):
    """Residual layer with embeddings and convolutions for downscaling."""

    residual_block_cls = EmbeddingsResidualBlock
    resize_cls = nn.Conv2d


class TransConvEResidualLayer(ConvResizeResidualLayerABC):
    """Residual layer with embeddings and Transposed convolutions for upscaling."""

    residual_block_cls = EmbeddingsResidualBlock
    resize_cls = nn.ConvTranspose2d
