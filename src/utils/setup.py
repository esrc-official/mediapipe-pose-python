from omegaconf import DictConfig
from hydra.utils import instantiate

from ..dataset_modules.dataset import Dataset
from ..architecture_modules.archimodule import ArchiModule
from .logger import Logger


class SetUp:
    def __init__(self, config: DictConfig):
        self.config = config

    def get_dataset_module(self) -> Dataset:
        dataset_module: Dataset = instantiate(
            self.config.dataset_module
        )
        return dataset_module

    def get_architecture_module(self) -> ArchiModule:
        architecture_module: ArchiModule = instantiate(
            self.config.architecture_module
        )
        return architecture_module

    def get_logger(self) -> Logger:
        logger: Logger = instantiate(
            self.config.logger
        )
        return logger
