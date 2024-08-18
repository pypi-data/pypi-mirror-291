from torch import nn

from .attention import CSA
from .conv import PreNormActConvBlock
from .residual import ResidualBlock


class LatentAlignLayer(nn.Sequential):
    """Hidden layer that proyect into the latent space.

    It's a Residual(Attention)Residual layer, plus
    an align conv block so the input and the output match the expected shapes

    Args:
        in_channels: input's channels
        out_channels: output's channels
        input_shape: tensor height and width
        attention: whether to use attention or not
        nonlinearity: nonlinearity to use in the residual blocks
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        input_shape: int,
        attention: bool = False,
        nonlinearity: nn.Module = None,
        **kwargs,
    ):
        r_channels = max(in_channels, out_channels)
        r1 = ResidualBlock(
            in_channels=r_channels,
            out_channels=r_channels,
            nonlinearity=None if attention else nonlinearity,
            **kwargs,
        )

        r2 = ResidualBlock(
            in_channels=r_channels,
            out_channels=r_channels,
            nonlinearity=nonlinearity,
            **kwargs,
        )

        conv_align = PreNormActConvBlock(
            in_channels=in_channels,
            out_channels=out_channels,
            nonlinearity=None,
            **kwargs,
        )

        attn = []
        if attention:
            attn = [
                CSA(
                    channels=r_channels,
                    height=input_shape,
                    width=input_shape,
                )
            ]

        blocks = [r1, *attn, r2]
        if in_channels > out_channels:
            blocks = [*blocks, conv_align]
        else:
            blocks = [conv_align, *blocks]

        super().__init__(*blocks)
