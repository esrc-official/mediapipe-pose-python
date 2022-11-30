from omegaconf import DictConfig

from ..utils.setup import SetUp


def test(config: DictConfig):
    setup = SetUp(config)

    dataset_module = setup.get_dataset_module()
    archi_module = setup.get_architecture_module()
    logger = setup.get_logger()

    archi_module.predict(dataset_module, logger)
