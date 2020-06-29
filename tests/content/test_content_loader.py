# st2
import os

from ultron8.content.loader import ContentPackLoader
from ultron8.content.loader import LOG
import pytest

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../resources"))


class ContentLoaderTest:
    def test_get_sensors(self):
        packs_base_path = os.path.join(RESOURCES_DIR, "packs/")
        loader = ContentPackLoader()
        pack_sensors = loader.get_content(
            base_dirs=[packs_base_path], content_type="sensors"
        )
        assert pack_sensors.get("pack1", None) is not None

    def test_get_sensors_pack_missing_sensors(self):
        loader = ContentPackLoader()
        fail_pack_path = os.path.join(RESOURCES_DIR, "packs/pack2")
        assert os.path.exists(fail_pack_path)
        assert loader._get_sensors(fail_pack_path) == None

    def test_invalid_content_type(self):
        packs_base_path = os.path.join(RESOURCES_DIR, "packs/")
        loader = ContentPackLoader()
        with pytest.raises(ValueError):
            loader.get_content(base_dirs=[packs_base_path], content_type="stuff")

    def test_get_content_multiple_directories(self, mocker):
        packs_base_path_1 = os.path.join(RESOURCES_DIR, "packs/")
        packs_base_path_2 = os.path.join(RESOURCES_DIR, "packs2/")
        base_dirs = [packs_base_path_1, packs_base_path_2]

        LOG.warning = mocker.Mock()

        loader = ContentPackLoader()
        sensors = loader.get_content(base_dirs=base_dirs, content_type="sensors")
        assert "pack1" in sensors  # from packs/
        assert "pack3" in sensors  # from packs2/

        # Assert that a warning is emitted when a duplicated pack is found
        expected_msg = (
            'Pack "pack1" already found in '
            '"%s/packs/", ignoring content from '
            '"%s/packs2/"' % (RESOURCES_DIR, RESOURCES_DIR)
        )
        LOG.warning.assert_called_once_with(expected_msg)

    def test_get_content_from_pack_success(self):
        loader = ContentPackLoader()
        pack_path = os.path.join(RESOURCES_DIR, "packs/pack1")

        sensors = loader.get_content_from_pack(
            pack_dir=pack_path, content_type="sensors"
        )
        assert sensors.endswith("packs/pack1/sensors")

    def test_get_content_from_pack_directory_doesnt_exist(self):
        loader = ContentPackLoader()
        pack_path = os.path.join(RESOURCES_DIR, "packs/pack100")

        message_regex = "Directory .*? doesn't exist"
        with pytest.raises(ValueError, match=message_regex):
            loader.get_content_from_pack(pack_dir=pack_path, content_type="sensors")

    def test_get_content_from_pack_no_sensors(self):
        loader = ContentPackLoader()
        pack_path = os.path.join(RESOURCES_DIR, "packs/pack2")

        result = loader.get_content_from_pack(
            pack_dir=pack_path, content_type="sensors"
        )
        assert result == None
