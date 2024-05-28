import os

from atomea.schemas.simulation.amber import Amber22Schema

from .conftest import TMP_DIR


def test_render_amber_to_yaml():
    schema_amber = Amber22Schema()
    yaml_path = os.path.join(TMP_DIR, "amber22.yml")
    schema_amber.to_yaml(yaml_path)


def test_render_amber_write_input():
    schema_amber = Amber22Schema()
    input_path = os.path.join(TMP_DIR, "amber22.in")
    schema_amber.write_input(input_path)
