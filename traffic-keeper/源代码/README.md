# Traffic Keeper 源代码

## 项目结构

```
app/
  server/
    traffic-keeper.sh   # 主运行脚本
    fetch-links.sh      # 链接获取脚本
    webserver.py        # Web 管理界面
  ui/
    config              # 应用中心打开按钮配置
    images/             # 应用图标
cmd/
  main                 # 启动/停止入口（系统调用）
  install_callback/init
  uninstall_callback/init
  upgrade_callback/init
  config_callback/init
config/
  privilege            # 运行权限配置
  resource             # 资源配置
manifest               # 应用清单
ICON.PNG               # 应用图标 (64x64)
ICON_256.PNG           # 应用图标 (256x256)
build.sh               # FPK 一键构建脚本
```

## 构建

在飞牛 NAS 上执行：

```bash
cd 源代码/
bash build.sh
```

## 飞牛 FPK 架构说明

| 目录/文件 | 部署路径 | 说明 |
|-----------|----------|------|
| `app/server/` | `/vol2/@appcenter/traffic-keeper/server/` | 应用主程序 |
| `app/ui/` | `/vol2/@appcenter/traffic-keeper/ui/` | 桌面入口配置 |
| `cmd/main` | `/var/apps/traffic-keeper/cmd/main` | 生命周期管理 |
| `config/` | `/vol2/@appcenter/traffic-keeper/config/` | 权限和资源 |
| `manifest` | `/var/apps/traffic-keeper/manifest` | 应用元数据 |
