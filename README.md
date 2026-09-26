# EIEM Blender 插件

在 Blender 中制作《明日方舟：终末地》的 EIEM Mod。导入 [AnimeStudio](https://github.com/ssice-a/AnimeStudio) 导出的 EIEM 资源，编辑模型、材质和贴图，再导出供 [EIEM 游戏插件](https://github.com/ssice-a/EIEM) 使用的 Mod 包。

## 功能

- 编辑模型、材质、贴图与 LOD；支持多个部件、材质槽和形态键。
- 为服装或部件制作款式切换，设置游戏快捷键和默认款式。
- 为形态键设置滑块及可选的快捷键，生成简单的游戏内控制界面。
- 只导出选中的资源；提供普通 Mod 包和仅网格包两种导出方式。
- 在插件设置中手动检查更新，可忽略指定版本。

## 安装

从 [Releases](https://github.com/ssice-a/EIEM-blender/releases) 下载 `EIEM_Blender_v*.zip`。在 Blender 的插件设置中选择“从磁盘安装”，直接选择 ZIP，然后启用插件。更新前先移除旧版，避免重复安装；请保存正在编辑的 `.blend` 工程。

## 制作 Mod

1. 在 AnimeStudio 中选中游戏 Prefab，导出 EIEM 源包。
2. 在 Blender 中选择 **文件 → 导入 → EIEM Mod 包**，打开源包里的 `mod.ini`。
3. 编辑模型、材质和贴图。需要款式切换时，在 **3D 视图 → N → EIEM → 网格切换**中创建款式并选择默认状态。形态键滑块可在网格数据属性中设置。
4. 选择要导出的 EIEM 网格，使用 **文件 → 导出 → EIEM Mod 包**。可在导出窗口选择 LOD 和“导出按键切换”。
5. 将导出的文件夹放入游戏目录下的 `plugin/mods/`，进游戏后按 F10 刷新。

“**导出按键切换**”默认勾选。取消后，Mod 使用你设置的默认款式，不导出款式或形态键快捷键；模型形态键、滑块和其他资源仍会导出。这个选项只影响本次导出，不会更改 `.blend` 工程中的设置。

只需模型、材质和贴图时，可选 **EIEM 仅网格包**。关闭网格的相机开关会在导出包中隐藏游戏原模型；眼睛和显示器开关只影响 Blender 中的预览。请将导出包保存到新的目录，保留 AnimeStudio 源包和 `.blend` 工程。

旧版 EIEM 源包需要使用当前 AnimeStudio 重新导出。有关安装游戏插件和使用现成 Mod 的说明，请看 [EIEM README](https://github.com/ssice-a/EIEM#readme)。

## TODO

- 扩展新增骨骼与物理效果的制作支持。
- 改进多角色制作体验。

## 鸣谢与声明

- 感谢 [AnimeStudio](https://github.com/Escartem/AnimeStudio) 及其贡献者。其他依赖的版权与许可证见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES)。
- 插件不包含游戏美术资产；游戏素材版权属于鹰角网络。使用前请阅读 [EIEM 用户协议与免责声明](https://github.com/ssice-a/EIEM#用户协议与免责声明)，自行承担使用风险。
