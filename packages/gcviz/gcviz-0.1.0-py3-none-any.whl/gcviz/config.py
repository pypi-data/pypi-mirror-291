class GlobalConfig:
    _config: dict[str, any] | None = None

    @classmethod
    def set(cls, config: dict[str, any]) -> None:

        if cls._config is not None:
            raise RuntimeError("Global config already set")
        cls._config = config

    @classmethod
    def get(cls, name: str | None = None) -> dict[str, any]:
        if cls._config is None:
            raise RuntimeError("Global config not set")
        if name is not None:
            if name not in cls._config:
                raise ValueError(f"Config {name} not found")
            return cls._config[name]
        return cls._config
