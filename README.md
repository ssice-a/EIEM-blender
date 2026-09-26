# EIEM Blender

EIEM 的 Blender 作者工具。它读取 AnimeStudio 解包出的 EIEM 资源，编辑网格、材质、贴图、LOD、款式和形态键，再导出给 EIEM DLL 使用的 Mod 包。

- DLL 与运行时协议：[ssice-a/EIEM](https://github.com/ssice-a/EIEM)
- 资源解包器：[ssice-a/AnimeStudio](https://github.com/ssice-a/AnimeStudio)
- Blender 插件：本仓库

三端通过文件协议连接，不互相复制源码。格式变化应先更新 EIEM 主仓库中的协议文档，再分别更新生产端和消费端。

插件设置里有“检查更新”按钮：手动查询本仓库最新正式 Release，显示版本及下载入口。
可以忽略某一版本，遇到下一版本仍会提示；插件不会自行下载或覆盖安装。

## 安装与开发

从 [EIEM Blender Releases](https://github.com/ssice-a/EIEM-blender/releases) 下载插件 ZIP。在 Blender 的插件设置中选择“从磁盘安装”，直接选择 ZIP；无需先解压。升级前在插件设置中移除旧版 EIEM，避免同时加载两份。

发布包应包含以下运行文件：

- `__init__.py`：Blender 插件入口。
- `eiem_blender_addon.py`：场景导入、导出编排和 UI。
- `eiem_format.py`：不依赖 Blender 的 EIEM 二进制与 INI 读取。
- `eiem_lod.py`：LOD 发现和导出规划。
- `eiem_blender_controls.py`：款式切换、形态键和生成 UI 的作者数据。
- `eiem_physics_*.py`：物理作者工具、源数据和文件格式。

开发目录为主工作区中的 `E:\vscode\EIEM\tools\Blender`。在 VS Code 中运行 **Blender: Start**，修改后运行 **Blender: Reload Addons**。不要同时安装旧版 ZIP 或单文件插件，否则 Blender 可能注册两份同名操作。

## 常用流程

1. 用 AnimeStudio 导出包含 `mod.ini` 的 EIEM 资源目录。
2. 在 Blender 选择 **文件 → 导入 → EIEM Mod 包**，选择该目录的 `mod.ini`。
3. 编辑需要替换的网格、材质和贴图。
4. 只选择本次要导出的 EIEM 网格。
5. 选择 **文件 → 导出 → EIEM Mod 包**；只改网格、材质和贴图时可用 **EIEM 仅网格包**。
6. 将导出目录放入 EIEM 的 `mods` 目录，在游戏内刷新。

导入窗口默认不显示物理文件选择。只有勾选“导入物理骨骼与碰撞体”后才显示该高级输入。

## 选择与显隐

- 导出器只处理所选网格，不自动补选同源物体或款式组成员。
- Blender 的相机开关表示游戏显隐：关闭时生成隐藏动作，不写该物体的网格资源。
- 眼睛和显示器开关只影响 Blender 预览。
- 同一个原 Mesh 拆成多块后，这些部件仍共享一个命中目标；需要保留的部件必须一起导出。
- 不要覆盖 AnimeStudio 的离线源包。把 `.blend` 当作后续编辑的作者工程。

## LOD

导出窗口可以选择 LOD0–LOD4，或导出当前工程中已发现的全部 LOD。插件只为真实存在于导入资源中的级别生成命中规则；缺失级别不会伪造资源。选中的模板只写出一份 Mesh，各目标 LOD 的 Render 规则共同引用它，因此几何、权重、bindpose 和源骨骼槽保持同一契约；各 LOD 也共享同一款式状态。

详细契约见 [Blender LOD 导出](https://github.com/ssice-a/EIEM/blob/main/docs/blender-lod-export.md)。

## 款式与形态键

3D 视图按 `N`，打开 **EIEM → 网格切换**：

- 从所选网格创建切换组，设置快捷键并记录多个款式。
- 相机开关记录游戏显隐；眼睛仅用于预览。
- 每个 Mod 的变量和状态独立。
- 可选的简单 UI 会生成 `ui.lua`；复杂布局可在导出后自行编辑。

形态键控制位于网格数据属性。新增形态键会自动进入导出计划；原生形态键需要主动接管。增大键和减小键按设定速度向上限或下限移动。

详细契约见 [切换与导出](https://github.com/ssice-a/EIEM/blob/main/docs/blender-switches.md) 和 [形态键](https://github.com/ssice-a/EIEM/blob/main/docs/shape-controls.md)。

## 材质与贴图

材质属性中的 **EIEM 材质** 面板可导入其他 EIEM `.mat`。插件保留源材质身份，只导出发生变化的参数和贴图。它不把任意 Blender 节点材质编译成游戏 Shader。

UV 接缝、顶点色、切线和多维 UV 会按面角拆分输出顶点，不修改 `.blend` 中的拓扑。详细规则见 [顶点数据契约](https://github.com/ssice-a/EIEM/blob/main/docs/vertex-data-contract.md)。

## 蒙皮与共享骨架

EIEMESH v6 保存每个局部骨骼槽的“源 Mesh 身份 + 原始槽号候选”。导出器保留全部原槽，只在末尾追加新增槽；新增槽必须能在同一 Armature 的原生 Mesh 供体中找到。DLL 在当前 NPC、UI 或大世界实例内，从对应原生 Mesh 的 `bones[]` 解析 Transform，因此不依赖三个 PFB 使用完全相同的骨骼名称，也不会跨实例借用骨骼。

当前每个顶点保存四个最强影响并归一化。缺失正权重骨骼、无权重面顶点或损坏的源槽会明确报错。旧 EIEMESH v2–v5 保留兼容读取，但 v2–v4 不具备跨 PFB 改名保证，应重新导入并导出为 v6。

详细契约见 [共享骨架绑定](https://github.com/ssice-a/EIEM/blob/main/docs/shared-skeleton-binding.md)。

## 物理作者工具

物理仍是独立演进的高级模块。普通 Mesh 导入导出无需启用它。需要物理时，可导入 AnimeStudio 的 `physics/components.json`，查看原生组和碰撞体，复制参数，并创建作者物理链。

物理 UI 中的 Group/Collider 数据是作者源数据；辅助几何只用于显示。完整原生物理图、无限平面和新增骨骼的运行时装配仍需按主仓库验证计划推进。

详细文档见 [物理作者 v2](https://github.com/ssice-a/EIEM/blob/main/docs/physics-authoring-v2.md)。

## 代码边界

依赖方向保持单向：

```text
eiem_format.py            纯文件格式
eiem_lod.py               纯 LOD 规划
eiem_blender_controls.py  纯作者状态与导出计划
           ↓
eiem_blender_addon.py     Blender 场景适配、导入导出编排、UI
           ↓
eiem_physics_*.py         可选物理作者模块
```

格式层和 LOD 层不导入 `bpy`，可以在普通 Python 中快速测试。场景层应优先使用 Blender 的 `foreach_get/foreach_set` 批量读写大数组，避免逐顶点跨越 Python/RNA 边界。

## 验证

普通 Python 检查：

```powershell
python -m unittest -v test_eiem_format.py
python -m compileall -q .
```

其余 `test_eiem_*.py` 是真实 Blender 集成测试，需要通过 Blender 的后台模式运行。发布工作流会把所有运行模块打进同一个插件 ZIP。
