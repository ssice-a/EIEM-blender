# Architecture

EIEM Blender 是三端管线中的作者端：AnimeStudio 生产原始 EIEM 资源，Blender 产生 Mod 资源，EIEM DLL 在游戏内消费这些文件。

## 模块

| 模块 | 责任 | 不应包含 |
|---|---|---|
| `eiem_format.py` | 二进制读写、INI 静态声明读取、安全路径 | `bpy`、场景对象、UI |
| `eiem_lod.py` | LOD 身份、发现和导出计划 | 文件写入、Blender UI |
| `eiem_blender_controls.py` | 款式与形态键作者状态、导出计划 | 网格二进制序列化 |
| `eiem_blender_addon.py` | 场景适配、导入导出编排、面板和操作 | 新的独立协议实现 |
| `eiem_physics_*.py` | 可选物理数据、作者 UI 和辅助显示 | 普通 Mesh 导出的必需依赖 |

## 约束

- 文件格式先进入纯模块，并由普通 Python 测试覆盖。
- Blender 对大型数组使用批量 RNA API；单对象操作才使用逐项 API。
- UI 默认只呈现完成当前任务所需的输入，高级输入由开关展开。
- 导出由选择集决定；不隐式扩大到同源网格或切换组。
- 骨骼槽顺序是协议身份，显示名称只是作者信息。
- 物理模块可以读取共享 Rig，但普通 Mesh 流程不依赖物理模块成功初始化。

## 下一步拆分

`eiem_blender_addon.py` 仍包含场景构建与包写入。后续只有在集成测试覆盖对应边界后，才继续拆成 `scene_import` 与 `package_export`；不为缩短文件而复制状态或增加双向依赖。
