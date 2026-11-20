# 飞牛 fnOS 第三方应用源（FnDepot V2）

个人维护的飞牛 fnOS 外部应用源，格式遵循 [FnDepot V2 规范](https://github.com/EWEDLCM/FnDepot)，仅收录自研且已在真机实测通过的应用。

仓库按应用分目录：根目录下每个应用一个目录（目录名即 `appname`），该应用的**当前版本**安装包、图标与预览图集中在内；**历史版本**安装包归档在同目录的 `history/` 子目录，并由 `fnpack.json` 的 `releases` 逐版本登记。

## 添加源

在 FnDepot 客户端（需 v0.0.7 或更高版本）中添加以下任一地址：

- GitHub 仓库根地址：`https://github.com/w5456448820/FnDepot`
- JSON 直链：`https://raw.githubusercontent.com/w5456448820/FnDepot/main/fnpack.json`

## 应用列表

| 应用 | 应用标识 | 最新版本 | 架构 | 服务端口 | 源码 | 测试状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 证件号生成器 | `zjhsql` | 1.0.1 | all（x86 / arm 通用） | 23180 | [id-number-generator](https://github.com/w5456448820/id-number-generator) | 包结构校验：通过<br>接口功能测试：通过<br>fnOS 实机安装：待复测 | 生成统一社会信用代码、组织机构代码与居民身份证号码，支持 GB/T 2260 三级行政区划联动与 GB 11643 校验位计算 |

- 应用标识即 `appname`，需与安装包 `manifest` 中的 `appname` 完全一致（区分大小写）。
- 源码含 `manifest`、`app/server`（生成算法与内置 http 服务）、`app/www`（单页前端）、`cmd` 生命周期脚本，纯 Python 标准库实现；改版后按其说明重新构建，再将产物更新到本仓库。

所有号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示使用。

## 版本管理约定

- 版本号遵循 SemVer。每发布一个新版本：在 `fnpack.json` 的 `apps.<appname>.releases` 下新增一个版本键，登记该版本 `changelog`、`updated_at` 与 `packages.<arch>`（`download_url` / `sha256` / `size`）。
- **已发布版本的安装包不可变**：一旦登记，对应 fpk 不再覆盖改写；功能或图标有任何改动一律递增版本号重新发布，避免客户端 hash 校验冲突。
- 安装包存放位置：最新版本放在应用目录根下（`<appname>/<appname>-<版本>-all.fpk`），历史版本统一归档到 `<appname>/history/`。
- 历史版本默认保留，客户端可回装旧版；单应用 `releases` 条目上限 100 个，超出需清理最旧归档。

### 版本历史（zjhsql）

| 版本 | 发布日期 | 状态 | 变更摘要 |
| --- | --- | --- | --- |
| 1.0.1 | 2026-11-20 | 当前 | 修复重装后图标显示异常（包内图标恢复为应用原始 256x256 图标），功能无变更，可覆盖升级 |
| 1.0.0 | 2026-11-20 | 历史归档 | 首个版本；x86 / arm 双包合并为 platform=all 单包。已知问题：包内图标取自 arm 包，重装后图标异常 |

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 目录结构

```
.
├── fnpack.json                       # V2 源索引（客户端唯一入口，含各版本登记）
├── CHANGELOG.md                      # 变更记录
├── README.md
└── zjhsql/                           # 应用目录：证件号生成器
    ├── zjhsql-1.0.1-all.fpk          # 当前版本
    ├── icon.png
    ├── previews/
    │   ├── preview_1_page.png
    │   └── preview_2_generate.png
    └── history/                      # 历史版本归档
        ├── zjhsql-1.0.0-all.fpk
        ├── zjhsql-1.0.0-x86.fpk      # 合并前 x86 单包（仅存档，未在 releases 登记）
        └── zjhsql-1.0.0-arm.fpk      # 合并前 arm 单包（仅存档，未在 releases 登记）
```

新增应用时按同一布局落位：`<appname>/{<appname>-<版本>-all.fpk, icon.png, previews/, history/}`，并在 `fnpack.json` 中补齐相对 URL。

## 安装包校验

| 文件 | 版本 | 架构 | 大小（Bytes） | SHA256 |
| --- | --- | --- | --- | --- |
| `zjhsql/zjhsql-1.0.1-all.fpk` | 1.0.1 | all | 90552 | `0658741b7358290b6d1dec2564cfadecbca3f0114892338ccfcd14005be5b21c` |
| `zjhsql/history/zjhsql-1.0.0-all.fpk` | 1.0.0 | all | 57466 | `b5211dce5c5f8d7e473b5680252495db4910fb8441cdd615c180356a54731430` |
| `zjhsql/history/zjhsql-1.0.0-x86.fpk` | 1.0.0 | x86 | 90588 | `6ac02f19dd93cf977bf22c7f9751cb8a146658043aebac381de75103975d0b89` |
| `zjhsql/history/zjhsql-1.0.0-arm.fpk` | 1.0.0 | arm | 58162 | `6a945e6af85ddf81ff0d013713d54bc483e2469aa43df5691b681103db7a2b82` |

当前发布版本包内仅含 shell 生命周期脚本、Python 标准库服务端与静态前端资源，不含任何架构相关二进制，因此按 `platform=all` 单包分发，x86 与 arm 设备通用。x86 / arm 两个单包为合并前形态，仅作历史存档。

## 说明

- 安装包未签名，安装时 fnOS 会提示「未经验证应用的安全提示」，需手动确认。
- 外部源由用户自行添加，源作者不对使用后果作担保，请自行评估风险。
