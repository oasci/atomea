from abc import ABC

import yaml


class IO(ABC):
    """Handles YAML inputs and outputs."""

    def from_yaml(self, yaml_paths: str | list[str]) -> None:
        """Update the instance's attributes from one or more YAML files.

        TODO: Need to fix with new Pydantic framework.

        Args:
            yaml_paths: A sequence of YAML file paths or a single YAML file path.

        Raises:
            FileNotFoundError: If any of the YAML files cannot be found.
        """
        if isinstance(yaml_paths, str):
            yaml_paths = [yaml_paths]
        for yaml_path in yaml_paths:
            with open(yaml_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)
                for key, value in yaml_data.items():
                    if key in self.__fields__:  # type: ignore # pylint: disable=no-member
                        setattr(self, key, value)

    def to_yaml(self, file_path: str) -> None:
        """Serialize a Pydantic BaseModel instance to a YAML file.

        TODO: Need to fix with new Pydantic framework.

        Args:
            file_path: Path to the YAML file to write the serialized data to.

        Raises:
            IOError: If the file cannot be written to.
        """
        config_dict = self.dict()  # type: ignore # pylint: disable=no-member
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, default_flow_style=False)
