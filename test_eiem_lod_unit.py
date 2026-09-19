import unittest

import eiem_lod


class Mesh:
    type = "MESH"

    def __init__(self, level):
        self.name = "BodyLOD%d" % level
        self.data = {
            "eiem_section": "MeshBodyLOD%d" % level,
            "eiem_asset": "BodyLOD%d" % level,
            "eiem_source": "assets/body_lod%d.fbx" % level,
            "eiem_target_asset": "BodyLOD%d" % level,
            "eiem_target_path": "assets/body_lod%d.fbx" % level,
        }
        self._values = {
            "eiem_render_asset": "BodyLOD%d" % level,
            "eiem_render_section": "RenderBodyLOD%d" % level,
            "eiem_author_package": "authoring/body",
        }

    def get(self, key, default=None):
        return self._values.get(key, default)

    def __getitem__(self, key):
        return self._values[key]

    def __contains__(self, key):
        return key in self._values


class LodTests(unittest.TestCase):
    def test_discovery_and_template_expansion(self):
        lod0, lod1 = Mesh(0), Mesh(1)
        candidates = [lod0, lod1]
        self.assertEqual(eiem_lod.discover_mesh_lods(lod0, candidates), {0, 1})

        plan = {
            "objects": [lod0],
            "groups": [],
            "bindings": {lod0: ("$style", [0])},
            "hidden": set(),
        }
        expanded = eiem_lod.expand_lod_plan(
            plan, [0, 1], candidates,
            lambda obj: ("source", obj.get("eiem_render_asset", "")),
        )
        self.assertEqual([eiem_lod.mesh_lod_level(obj)
                          for obj in expanded["objects"]], [0, 1])
        self.assertEqual(expanded["bindings"][expanded["objects"][1]],
                         ("$style", [0]))

    def test_missing_lod_is_not_invented(self):
        lod0 = Mesh(0)
        plan = {"objects": [lod0], "groups": [], "bindings": {}, "hidden": set()}
        with self.assertRaisesRegex(ValueError, "不存在"):
            eiem_lod.expand_lod_plan(
                plan, [4], [lod0], lambda obj: ("source", obj.name))


if __name__ == "__main__":
    unittest.main()
