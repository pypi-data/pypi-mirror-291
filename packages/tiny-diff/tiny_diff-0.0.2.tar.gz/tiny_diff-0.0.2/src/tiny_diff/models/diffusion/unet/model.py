import torch
from torch import nn
from typing_extensions import override

from tiny_diff.models.conv_model import ConvModel
from tiny_diff.modules import PreNormActConvBlock, RARBlock

from .layers import DownUNetLayer, TimeEmbedding, UNetLayer, UNetSkipLayer, UpUNetLayer


class UNet(ConvModel):
    """UNet model used for diffusion tasks.

    Args:
        time_channels: channels of the time embedding dimension
        attn_at_layer: list of layer indexes in which attention should be used
        zero_init: whether to init weights to zero or not
    """

    def __init__(
        self,
        time_channels: int = None,
        attn_at_layer: list[bool] = None,
        zero_init: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.attn_at_layer = attn_at_layer or []
        if self.attn_at_layer and len(self.attn_at_layer) != len(self.channel_mult):
            raise ValueError("Length of self.attn_at_layer must match number of layers")

        self.time_channels = time_channels or self.base_channels * 4
        self.zero_init = zero_init
        self.conv_in = PreNormActConvBlock(
            **self.conv_kwargs(
                in_ch=self.input_channels,
                out_ch=self.base_channels,
                nonlinearity=None,
                scale_factor=None,
                drop_p=0,
                num_groups=None,
            )
        )
        self.current_shape = self.input_resolution
        # Down blocks
        self.down = nn.ModuleList(self._get_down_blocks())

        # Mid block
        mid_channels = self.channels[-1]
        mid_shape = self.current_shape
        self.middle = RARBlock(
            in_channels=mid_channels,
            out_channels=mid_channels,
            embed_channels=self.time_channels,
            input_shape=mid_shape,
            kernel_size=self.kernel_size,
            padding="same",
            num_groups=self.num_groups,
            scale_factor=None,
        )
        self.up = nn.ModuleList(self._get_up_blocks())

        self.conv_out = PreNormActConvBlock(
            **self.conv_kwargs(
                self.up_channels[-1],
                self.input_channels,
                scale_factor=None,
                attention=None,
                drop_p=0,
            )
        )

        self.time_emb = TimeEmbedding(self.time_channels)

    @property
    def r_channels(self):
        """Channels property reversed."""
        return self.channels[::-1]

    @property
    def down_channels(self) -> list[int]:
        """Channels of the first half of the UNet."""
        return [self.base_channels, *self.conv_channels]

    @property
    def up_channels(self) -> list[int]:
        """Channels of the second half of the UNet."""
        return self.down_channels[::-1]

    def _get_down_blocks(self) -> list[nn.Module]:
        down_in_chs = self.down_channels[:-1]
        down_out_chs = self.down_channels[1:]
        down = []
        for i, (ch_in, ch_out, attn) in enumerate(
            zip(down_in_chs, down_out_chs, self.attn_at_layer)
        ):
            final_block = i == (len(down_in_chs) - 1)
            layer_cls = UNetLayer if final_block else DownUNetLayer
            layer = layer_cls(
                **self.res_kwargs(
                    ch_in,
                    ch_out,
                    input_shape=self.current_shape,
                    attention=attn,
                    pop=["scale_factor"] if final_block else [],
                )
            )
            down.append(layer)
            self.current_shape = int(self.current_shape / self.factor)
        return down

    def _get_up_blocks(self) -> list[nn.Module]:
        up_in_chs = self.up_channels[1:]
        up_out_chs = self.up_channels[:-1]
        attn_at_up_layer = self.attn_at_layer[::-1]
        skip_chs = [up_out_chs[0]] + up_out_chs[:-1]
        # Up blocks
        up = []
        for i, (ch_in, ch_out, attn, ch_skip) in enumerate(
            zip(up_in_chs, up_out_chs, attn_at_up_layer, skip_chs)
        ):
            final_block = i == (len(up_in_chs) - 1)
            layer_cls = UNetSkipLayer if final_block else UpUNetLayer
            layer = layer_cls(
                **self.up_res_kwargs(
                    ch_in,
                    ch_out,
                    skip_in_channels=ch_skip,
                    skip_out_channels=0,
                    input_shape=self.current_shape,
                    attention=attn,
                    pop=["scale_factor"] if final_block else [],
                )
            )
            up.append(layer)
            self.current_shape = int(self.current_shape * self.factor)
        return up

    @override
    def conv_kwargs(
        self, in_ch: int, out_ch: int, pop: list[str] = None, **kwargs
    ) -> dict:
        return super().conv_kwargs(
            in_ch, out_ch, pop, zero_init=self.zero_init, **kwargs
        )

    @override
    def res_kwargs(self, *args, **kwargs):
        return super().res_kwargs(*args, embed_channels=self.time_channels, **kwargs)

    def up_res_kwargs(self, *args, **kwargs):
        """Kwargs for residual layers of the second half of the net."""
        kwgs = self.res_kwargs(*args, **kwargs)
        kwgs["n_blocks"] += 1
        return kwgs

    @override
    def forward(self, x: torch.Tensor, t: torch.Tensor):
        t = self.time_emb(t)

        h = self.conv_in(x)
        h_stack = [h]

        for layer in self.down:
            h, hs = layer(h, t)
            h_stack.extend(hs)

        h = self.middle(h, t)

        for layer in self.up:
            n_pop = len(layer.blocks)
            s, h_stack = h_stack[-n_pop:], h_stack[:-n_pop]
            h = layer(h, s, t)

        return self.conv_out(h)
