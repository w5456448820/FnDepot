# 飞牛 fnOS 第三方应用源（FnDepot V2）

个人维护的飞牛 fnOS 外部应用源，格式遵循 [FnDepot V2 规范](https://github.com/EWEDLCM/FnDepot)，仅收录自研且已在真机实测通过的应用。

仓库按「应用分类」组织目录：`packages/` 与 `assets/` 下均以分类目录（`develop/`、`system/`、`media/` …）分层，新增应用时归入对应分类目录即可；客户端侧的分类筛选由 `fnpack.json` 中每个应用的 `categories` 字段驱动。

## 添加源

在 FnDepot 客户端（需 v0.0.7 或更高版本）中添加以下任一地址：

- GitHub 仓库根地址：`https://github.com/w5456448820/FnDepot`
- JSON 直链：`https://raw.githubusercontent.com/w5456448820/FnDepot/main/fnpack.json`

## 分类导航

| 分类 | 目录标识 | 应用数 | 应用 |
| --- | --- | --- | --- |
| 影音娱乐 | `media/` | 0 | — |
| 系统工具 | `system/` | 0 | — |
| **编程开发** | `develop/` | **1** | 证件号生成器 |
| AI赋能 | `ai/` | 0 | — |
| 生活服务 | `life/` | 0 | — |
| 智能智控 | `smart/` | 0 | — |
| 教育学习 | `edu/` | 0 | — |
| 游戏地带 | `game/` | 0 | — |
| 硬件驱动 | `driver/` | 0 | — |

## 应用列表（按分类）

### 编程开发

| 应用 | appname | 版本 | 架构 | 服务端口 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 证件号生成器 | `zjhsql` | 1.0.0 | x86 / arm | 23180 | 生成统一社会信用代码、组织机构代码与居民身份证号码，支持 GB/T 2260 三级行政区划联动与 GB 11643 校验位计算 |

所有号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示使用。

## 分类字段说明

- `categories` 只能取以下九个固定值，不能自造：`影音娱乐`、`系统工具`、`编程开发`、`AI赋能`、`生活服务`、`智能智控`、`教育学习`、`游戏地带`、`硬件驱动`。
- 最多填写两个，**数组第一项为主分类**，客户端分类页以主分类归位。
- 「全部」只是客户端界面筛选项，不得写入 `categories`。

## 目录结构

```
.
├── fnpack.json                       # V2 源索引（客户端唯一入口）
├── packages/
│   └── develop/                      # 按分类分层：编程开发
│       ├── zjhsql-1.0.0-x86.fpk
│       └── zjhsql-1.0.0-arm.fpk
├── assets/
│   └── develop/
│       └── zjhsql/                   # 按分类/应用分层
│           ├── icon.png
│           └── previews/
│               ├── preview_1_page.png
│               └── preview_2_generate.png
└── src/
    └── zjhsql/                       # 证件号生成器 FPK 工程源码
```

新增应用时遵循同一规则：`packages/<分类标识>/<appname>-<版本>-<架构>.fpk`、`assets/<分类标识>/<appname>/icon.png` 与 `assets/<分类标识>/<appname>/previews/*.png`，并同步更新 `fnpack.json` 中的相对 URL。

## 源码

FPK 打包工程源码位于 [`src/zjhsql`](src/zjhsql)，含 `manifest`、`app/server`（生成算法与内置 http 服务）、`app/www`（单页前端）、`cmd` 生命周期脚本，纯 Python 标准库实现。构建方式见 [src/zjhsql/README.md](src/zjhsql/README.md)。

## 安装包校验

| 文件 | 架构 | 大小（Bytes） | SHA256 |
| --- | --- | --- | --- |
| `packages/develop/zjhsql-1.0.0-x86.fpk` | x86 | 90588 | `6ac02f19dd93cf977bf22c7f9751cb8a146658043aebac381de75103975d0b89` |
| `packages/develop/zjhsql-1.0.0-arm.fpk` | arm | 58162 | `6a945e6af85ddf81ff0d013713d54bc483e2469aa43df5691b681103db7a2b82` |

两个包内容一致，均为纯 Python 标准库实现的网页服务，仅 manifest 的 `platform` 字段不同。

## 测试状态

| 架构 | 状态 |
| --- | --- |
| x86 | 已在 fnOS（MEmini-13F2）实机安装、启动并通过功能测试 |
| arm | 已构建并通过结构与 manifest 校验，尚未在 arm 设备实测 |

## 说明

- 安装包未签名，安装时 fnOS 会提示「未经验证应用的安全提示」，需手动确认。
- 外部源由用户自行添加，源作者不对使用后果作担保，请自行评估风险。
