# 变更记录

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 SemVer。

## [1.0.1] - 2026-11-20

### 修复

- 修复在 fnOS 中重装后应用图标显示异常的问题：包内 `ICON.PNG`、`ICON_256.PNG`、`ui/images/icon_256.png`、`ui/images/icon_64.png` 恢复为应用原始 256x256 图标（此前误用了 arm 包中的另一张图形）。

### 变更

- 版本号由 1.0.0 递增至 1.0.1（包内 `manifest.version` 同步），功能、接口与数据结构与 1.0.0 完全一致，可直接覆盖升级。
- 仓库引入历史版本目录：`.fpk` 归档到 `<appname>/history/`，`fnpack.json` 的 `releases` 逐版本登记 `download_url` / `sha256` / `size`。

## [1.0.0] - 2026-11-20

### 新增

- 首个版本：网页版证件号生成器，23180 端口提供网页服务，支持统一社会信用代码、组织机构代码与居民身份证号码生成。
- 支持 GB/T 2260 三级行政区划联动，GB 11643 校验位计算，内置随机虚构数据生成。

### 变更

- 原 x86 / arm 双包合并为 `platform=all` 单包（包内仅含脚本与静态资源，无架构相关二进制），两类设备通用。
- 两者合并前的原始单包（`zjhsql-1.0.0-x86.fpk`、`zjhsql-1.0.0-arm.fpk`）归档至 `zjhsql/history/`，仅作存档，不在 `releases` 中登记。

### 已知问题

- 合并时包内图标取自 arm 包，重装后图标显示为另一图形，已在 1.0.1 修复。
