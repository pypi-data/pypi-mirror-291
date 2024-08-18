from typing import Optional, Union

import torch
from typing_extensions import override


class DDPMScheduler:
    """Denoise Diffusion Probabilistic Model scheduler.

    Provides functionality to do the forward and backward diffusion process.

    Args:
        num_train_steps: number of steps to use in training
        num_inference_steps: number of steps to use in inference
        beta_start: Beta0 value
        beta_end: BetaT value
    """

    def __init__(
        self,
        num_train_steps: int = 1000,
        num_inference_steps: Optional[int] = None,
        beta_start: float = 0.0001,
        beta_end: float = 0.02,
        clip_range: Optional[float] = None,
    ):
        self._betas = self.set_betas(
            beta_start, beta_end, num_train_steps, dtype=torch.float32
        )
        self.clip_range = clip_range
        self.init_noise_sigma = 1.0
        self._num_inference_steps = num_inference_steps

    def _get_betas(self, start: float, end: float, *args, **kwargs) -> torch.Tensor:
        return torch.linspace(start, end, *args, **kwargs)

    def _set_alphas(self):
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)

    @property
    def betas(self):
        """Beta schedule."""
        return self._betas

    def set_betas(self, beta_start: float, beta_end: float, n_steps: int):
        """Sets the beta schedule."""
        self._betas = self._get_betas(
            beta_start, beta_end, n_steps, dtype=torch.float32
        )
        self._set_alphas()
        self.timesteps = self.get_timesteps()

    @property
    def num_train_steps(self) -> int:
        """Diffusion steps to use in train."""
        return len(self.betas)

    @property
    def num_inference_steps(self) -> int:
        """Diffusion steps to use in inference."""
        return self._num_inference_steps or self.num_train_steps

    @property
    def clip_sample(self) -> bool:
        """Whether to clip a sample or not."""
        return self.clip_range is not None

    @property
    def _timesteps_ratio(self):
        return self.num_train_steps // self.num_inference_steps

    def _previous_timestep(self, t) -> int:
        return t - self._timesteps_ratio

    def step(
        self,
        x: torch.Tensor,
        t: int,
        sample: torch.Tensor,
        generator=None,
    ) -> dict[str, torch.Tensor]:
        """Predict noise at time t-1 given time t.

        Args:
            x: The direct output from learned diffusion model.
            t: The current discrete timestep in the diffusion process.
            sample: A current instance of a sample created by the diffusion process.
            generator : A random number generator.
        """
        prev_t = self._previous_timestep(t)

        alpha_prod_t = self.alphas_cumprod[t]
        alpha_prod_t_prev = (
            self.alphas_cumprod[prev_t] if prev_t >= 0 else torch.tensor(1.0)
        )
        beta_prod_t = 1 - alpha_prod_t
        beta_prod_t_prev = 1 - alpha_prod_t_prev
        current_alpha_t = alpha_prod_t / alpha_prod_t_prev
        current_beta_t = 1 - current_alpha_t

        # Substract the noise
        pred_original_sample = (sample - beta_prod_t ** (0.5) * x) / alpha_prod_t ** (
            0.5
        )

        if self.clip_sample:
            pred_original_sample = pred_original_sample.clamp(
                -self.clip_range, self.clip_range
            )

        pred_original_sample_coeff = (
            alpha_prod_t_prev ** (0.5) * current_beta_t
        ) / beta_prod_t
        current_sample_coeff = current_alpha_t ** (0.5) * beta_prod_t_prev / beta_prod_t

        pred_prev_sample = (
            pred_original_sample_coeff * pred_original_sample
            + current_sample_coeff * sample
        )

        std = 0
        if t > 0:
            variance_noise = torch.randn(
                x.shape,
                generator=generator,
                device=x.device,
                dtype=x.dtype,
            )

            std = (self._get_variance(t) ** 0.5) * variance_noise

        pred_prev_sample = pred_prev_sample + std

        return {
            "prev_sample": pred_prev_sample,
            "pred_original_sample": pred_original_sample,
        }

    def _get_variance(self, t):
        prev_t = self._previous_timestep(t)
        alpha_prod_t = self.alphas_cumprod[t]
        alpha_prod_t_prev = (
            self.alphas_cumprod[prev_t] if prev_t >= 0 else torch.tensor(1.0)
        )
        current_beta_t = 1 - alpha_prod_t / alpha_prod_t_prev
        variance = (1 - alpha_prod_t_prev) / (1 - alpha_prod_t) * current_beta_t
        variance = torch.clamp(variance, min=1e-20)
        return variance

    def get_timesteps(
        self,
        n_steps: Optional[int] = None,
        device: Optional[Union[str, torch.device]] = None,
    ):
        """Sets the discrete timesteps.

        These are used for the diffusion chain (to be run before inference).

        Args:
            n_steps: # of diffusion steps used when generating samples
            device: The device to which the timesteps may be moved to.
        """
        n_steps = n_steps or self.num_train_steps
        return (
            (torch.arange(0, n_steps) * self._timesteps_ratio).int().flip(-1).to(device)
        )

    def add_noise(
        self,
        original_samples: torch.Tensor,
        noise: torch.Tensor,
        timesteps: torch.IntTensor,
    ) -> torch.Tensor:
        """Adds noise in the forward diffusion process."""
        self.alphas_cumprod = self.alphas_cumprod.to(device=original_samples.device)
        alphas_cumprod = self.alphas_cumprod.to(dtype=original_samples.dtype)
        timesteps = timesteps.to(original_samples.device)

        sqrt_alpha_prod = alphas_cumprod[timesteps] ** 0.5
        sqrt_alpha_prod = sqrt_alpha_prod.flatten()
        while len(sqrt_alpha_prod.shape) < len(original_samples.shape):
            sqrt_alpha_prod = sqrt_alpha_prod.unsqueeze(-1)

        sqrt_one_minus_alpha_prod = (1 - alphas_cumprod[timesteps]) ** 0.5
        sqrt_one_minus_alpha_prod = sqrt_one_minus_alpha_prod.flatten()
        while len(sqrt_one_minus_alpha_prod.shape) < len(original_samples.shape):
            sqrt_one_minus_alpha_prod = sqrt_one_minus_alpha_prod.unsqueeze(-1)

        noisy_samples = (
            sqrt_alpha_prod * original_samples + sqrt_one_minus_alpha_prod * noise
        )
        return noisy_samples


class LatentDDPMScheduler(DDPMScheduler):
    """DDPM scheduler with original latent diffusion beta scheduler."""

    @override
    def _get_betas(self, start: float, end: float, *args, **kwargs) -> torch.Tensor:
        return super()._get_betas(start**0.5, end**0.5, *args, **kwargs) ** 2
