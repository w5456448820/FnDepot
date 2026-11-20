# 飞牛 fnOS 第三方应用源（FnDepot V2）

个人维护的飞牛 fnOS 外部应用源，格式遵循 [FnDepot V2 规范](https://github.com/EWEDLCM/FnDepot)，仅收录自研且已在真机实测通过的应用。

仓库按应用分目录：根目录下每个应用一个目录（目录名即 `appname`），该应用的安装包、图标与预览图集中在内。

## 添加源

在 FnDepot 客户端（需 v0.0.7 或更高版本）中添加以下任一地址：

- GitHub 仓库根地址：`https://github.com/w5456448820/FnDepot`
- JSON 直链：`https://raw.githubusercontent.com/w5456448820/FnDepot/main/fnpack.json`

## 应用列表

| 应用 | 应用标识 | 版本 | 架构 | 服务端口 | 源码 | 测试状态 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 证件号生成器 | `zjhsql` | 1.0.0 | all（x86 / arm 通用） | 23180 | [id-number-generator](https://github.com/w5456448820/id-number-generator) | 包结构校验：通过<br>接口功能测试：通过<br>fnOS 实机安装：待复测 | 生成统一社会信用代码、组织机构代码与居民身份证号码，支持 GB/T 2260 三级行政区划联动与 GB 11643 校验位计算 |

- 应用标识即 `appname`，需与安装包 `manifest` 中的 `appname` 完全一致（区分大小写）。
- 源码含 `manifest`、`app/server`（生成算法与内置 http 服务）、`app/www`（单页前端）、`cmd` 生命周期脚本，纯 Python 标准库实现；改版后按其说明重新构建，再将产物更新到本仓库。

所有号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示使用。

## 目录结构

```
.
├── fnpack.json                       # V2 源索引（客户端唯一入口）
└── zjhsql/                           # 应用目录：证件号生成器
    ├── zjhsql-1.0.0-all.fpk
    ├── icon.png
    └── previews/
        ├── preview_1_page.png
        └── preview_2_generate.png
```

新增应用时按同一布局落位：`<appname>/{<appname>-<版本>-all.fpk, icon.png, previews/}`，并在 `fnpack.json` 中补齐相对 URL。

## 安装包校验

| 文件 | 架构 | 大小（Bytes） | SHA256 |
| --- | --- | --- | --- |
| `zjhsql/zjhsql-1.0.0-all.fpk` | all | 90187 | `3fc0637c9593f08016d271d35bbd4b989f2331e157b876ccb14da9c0555784c0` |

包内仅含 shell 生命周期脚本、Python 标准库服务端与静态前端资源，不含任何架构相关二进制，因此按 `platform=all` 单包分发，x86 与 arm 设备通用。

## 说明

- 安装包未签名，安装时 fnOS 会提示「未经验证应用的安全提示」，需手动确认。
- 外部源由用户自行添加，源作者不对使用后果作担保，请自行评估风险。
