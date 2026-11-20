# 飞牛 fnOS 第三方应用源（FnDepot V2）

个人维护的飞牛 fnOS 外部应用源，格式遵循 [FnDepot V2 规范](https://github.com/EWEDLCM/FnDepot)，仅收录自研且已在真机实测通过的应用。

## 添加源

在 FnDepot 客户端（需 v0.0.7 或更高版本）中添加以下任一地址：

- GitHub 仓库根地址：`https://github.com/w5456448820/FnDepot`
- JSON 直链：`https://raw.githubusercontent.com/w5456448820/FnDepot/main/fnpack.json`

## 应用列表

| 应用 | appname | 版本 | 架构 | 服务端口 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 证件号生成器 | `zjhsql` | 1.0.0 | x86 | 23180 | 生成统一社会信用代码、组织机构代码与居民身份证号码，支持 GB/T 2260 三级行政区划联动与 GB 11643 校验位计算 |

所有号码均为随机虚构，仅供软件开发测试、系统联调与数据脱敏演示使用。

## 目录结构

```
.
├── fnpack.json                  # V2 源索引
├── packages/                    # FPK 安装包
│   └── zjhsql-1.0.0-x86.fpk
└── assets/
    ├── icons/                   # 应用图标
    └── previews/                # 应用预览图
```

## 安装包校验

| 文件 | 大小（Bytes） | SHA256 |
| --- | --- | --- |
| `packages/zjhsql-1.0.0-x86.fpk` | 90588 | `6ac02f19dd93cf977bf22c7f9751cb8a146658043aebac381de75103975d0b89` |

## 说明

- 安装包未签名，安装时 fnOS 会提示「未经验证应用的安全提示」，需手动确认。
- 外部源由用户自行添加，源作者不对使用后果作担保，请自行评估风险。
