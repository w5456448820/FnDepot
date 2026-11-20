# 飞牛 fnOS 第三方应用源（FnDepot V2）

个人维护的飞牛 fnOS 外部应用源，格式遵循 [FnDepot V2 规范](https://github.com/EWEDLCM/FnDepot)，仅收录自研且已在真机实测通过的应用。

仓库按应用分目录：根目录下每个应用一个目录（目录名即 `appname`），该应用的安装包、图标与预览图集中在内。应用所属分类不体现在目录上，由 `fnpack.json` 中每个应用的 `categories` 字段决定，客户端据此在分类页归类展示。

## 添加源

在 FnDepot 客户端（需 v0.0.7 或更高版本）中添加以下任一地址：

- GitHub 仓库根地址：`https://github.com/w5456448820/FnDepot`
- JSON 直链：`https://raw.githubusercontent.com/w5456448820/FnDepot/main/fnpack.json`

## 应用列表

| 分类 | 应用 | appname | 版本 | 架构 | 服务端口 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 编程开发 | 证件号生成器 | `zjhsql` | 1.0.0 | all（x86 / arm 通用） | 23180 | 生成统一社会信用代码、组织机构代码与居民身份证号码，支持 GB/T 2260 三级行政区划联动与 GB 11643 校验位计算 |

所有号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示使用。

## 分类字段说明

- `categories` 只能取以下九个固定值，不能自造：`影音娱乐`、`系统工具`、`编程开发`、`AI赋能`、`生活服务`、`智能智控`、`教育学习`、`游戏地带`、`硬件驱动`。
- 最多填写两个，**数组第一项为主分类**，客户端分类页以主分类归位。
- 「全部」只是客户端界面筛选项，不得写入 `categories`。
- 分类只存在于 JSON 中，不再用目录区分；新增应用时按应用建目录、按分类填字段即可。

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

新增应用时按同一布局落位：`<appname>/{<appname>-<版本>-all.fpk, icon.png, previews/}`，并在 `fnpack.json` 中补齐 `categories` 与相对 URL。

## 源码

FPK 打包工程源码不随本源仓库分发，统一维护在独立仓库：[w5456448820/id-number-generator](https://github.com/w5456448820/id-number-generator)。

该仓库含 `manifest`、`app/server`（生成算法与内置 http 服务）、`app/www`（单页前端）、`cmd` 生命周期脚本，纯 Python 标准库实现；改版后按其说明重新构建，再将产物更新到本仓库即可。

## 安装包校验

| 文件 | 架构 | 大小（Bytes） | SHA256 |
| --- | --- | --- | --- |
| `zjhsql/zjhsql-1.0.0-all.fpk` | all | 57466 | `b5211dce5c5f8d7e473b5680252495db4910fb8441cdd615c180356a54731430` |

包内仅含 shell 生命周期脚本、Python 标准库服务端与静态前端资源，不含任何架构相关二进制，因此按 `platform=all` 单包分发，x86 与 arm 设备通用。

## 测试状态

| 项目 | 状态 |
| --- | --- |
| 包结构校验 | 通过 —— tar.gz 可正常解包；顶层与 `app.tgz` 内条目、权限位与已实机验证的 x86 包逐项一致；`manifest` 的 `checksum` 与包内 `app.tgz` 的 MD5 一致 |
| 接口功能测试 | 通过 —— `/api/health`、`/api/districts`（31 个省级行政区）、`/api/generate`（`scc` / `org` / `id` 三类，含地区码、出生日期、性别定制）均返回预期结果 |
| fnOS 实机安装 | 待复测 —— all 单包尚未在 fnOS 设备上执行安装与启动验证 |

## 说明

- 安装包未签名，安装时 fnOS 会提示「未经验证应用的安全提示」，需手动确认。
- 外部源由用户自行添加，源作者不对使用后果作担保，请自行评估风险。
