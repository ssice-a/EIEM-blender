import tempfile
import unittest
from pathlib import Path

import eiem_format


class FormatTests(unittest.TestCase):
    def test_writer_reader_round_trip(self):
        writer = eiem_format.Writer()
        writer.i32(-7)
        writer.u32(0xFEEDBEEF)
        writer.f32(1.25)
        writer.string("裙子")
        writer.floats((1.0, 2.0, 3.0))

        reader = eiem_format.Reader(bytes(writer.data))
        self.assertEqual(reader.i32(), -7)
        self.assertEqual(reader.u32(), 0xFEEDBEEF)
        self.assertAlmostEqual(reader.f32(), 1.25)
        self.assertEqual(reader.string(), "裙子")
        self.assertEqual(reader.floats(), [1.0, 2.0, 3.0])
        self.assertEqual(reader.pos, len(reader.data))

    def test_safe_path_rejects_package_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                eiem_format.safe_path(root, "meshes/body.mesh"),
                (root / "meshes" / "body.mesh").resolve(),
            )
            with self.assertRaisesRegex(ValueError, "escapes package"):
                eiem_format.safe_path(root, "../outside.mesh")

    def test_parse_ini_ignores_runtime_control_flow(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "mod.ini").write_text(
                "[RenderBody]\n"
                "mesh = ResourceBody\n"
                "if $state == 1\n"
                "  draw = false\n"
                "else\n"
                "  draw = true\n"
                "endif\n"
                "[ResourceBody]\n"
                "path = meshes/body.mesh\n",
                encoding="utf-8",
            )

            parser = eiem_format.parse_ini(root)
            self.assertEqual(parser["RenderBody"]["mesh"], "ResourceBody")
            self.assertNotIn("draw", parser["RenderBody"])
            self.assertEqual(parser["ResourceBody"]["path"], "meshes/body.mesh")


if __name__ == "__main__":
    unittest.main()
