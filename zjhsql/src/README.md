# 证件号生成器 (zjhsql) — fnOS FPK 源码

飞牛 fnOS 应用「证件号生成器」的完整打包工程源码。原 Windows tkinter 桌面工具改造为网页版 FPK 应用，安装后在应用中心启动，通过浏览器访问使用。

> 所有生成号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示，不得用于任何真实业务场景。

## 目录结构

```
manifest                应用元信息（appname/version/platform/service_port 等）
ICON.PNG / ICON_256.PNG 应用图标
app/server/idgen.py     号码生成核心（统一社会信用代码、组织机构代码、身份证号、GB/T 2260 区划库）
app/server/pca-code.json  省市区三级行政区划码表（2978 条区县数据）
app/server/server.py    内置 http.server 后端（Unix socket / TCP 双模式，剥离 GATEWAY_PREFIX）
app/www/index.html      单页前端（区划联动、批量生成、校验位计算）
app/ui/                 应用中心入口配置与图标
cmd/                    生命周期脚本：main / install_* / uninstall_* / upgrade_* / config_*
config/                 privilege、resource 声明
wizard/install          安装向导文案
```

## 运行依赖

- Python 3（仅标准库：`http.server`、`json`、`random`、`argparse` 等，无第三方包）
- 默认服务端口 `23180`（`manifest` 中 `service_port` 与 `checkport = true`）

## 本地调试

```bash
python3 app/server/server.py --port 23180
# 浏览器打开 http://127.0.0.1:23180/
```

fnOS 环境下由 `cmd/main` 探测 `python3` 后启动服务，`server.py` 支持通过 Unix socket 与网关前缀（`GATEWAY_PREFIX`）对接。

## 构建 FPK

```bash
# 在 Linux（推荐 WSL）下使用 linux-amd64 版 fnpack
fnpack build -d . --nosign
```

产物为 `zjhsql-<version>.fpk`，可分架构（x86 / arm）分别构建并发布。本仓库根目录的 `fnpack.json` 为 FnDepot V2 源索引，指向 `packages/` 下的正式分发包。

## 生成算法说明

- 行政区划码：GB/T 2260 三级联动，数据见 `app/server/pca-code.json`
- 居民身份证号：GB 11643 十八位结构（6 位区划 + 8 位出生日期 + 3 位顺序码 + 1 位校验位，模 11-2 校验）
- 统一社会信用代码：18 位，含登记管理部门码、机构类别码、组织机构代码（GB 11714）与校验位
- 组织机构代码：8 位本体码 + 1 位校验位

## 许可

源码仅供学习与测试用途，请遵守当地法律法规，禁止用于伪造证件或欺诈行为。
