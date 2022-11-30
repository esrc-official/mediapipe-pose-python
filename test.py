import hydra
from omegaconf import OmegaConf

from src.engine.engine import test


@hydra.main(config_path="configs", config_name="customized_basic_mediapipe_pose_test.yaml")
def main(config):
    print(OmegaConf.to_yaml(config))
    return test(config)


if __name__ == "__main__":
    main()
