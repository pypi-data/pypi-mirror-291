import torch
from torch import nn
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
    def hadamard(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """Performs hadamard product."""
        return A * B

    @override
    def forward(self, x: torch.Tensor, e: torch.Tensor = None):
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
