from typing import Any, Optional


class NonLinearityGenerator:
    """Factory class for non linearity layers.

    Args:
        cls: non linearity class.
        init_args: positional args for cls.
        init_kwargs: keyword args for cls.
    """

    def __init__(
        self,
        cls: type,
        init_args: Optional[list[Any]] = None,
        init_kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        self.cls = cls
        self.init_args = init_args or []
        self.init_kwargs = init_kwargs or {}

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Instantiates an object of type cls and returns it."""
        return self.cls(*self.init_args, *args, **self.init_kwargs, **kwargs)
