#!/bin/bash
# Traffic Keeper FPK 构建脚本（在飞牛 NAS 上运行）
set -e
APP_NAME="traffic-keeper"
VERSION="1.0.2"
BUILD_DIR="/tmp/fpk-build-${APP_NAME}"
echo "=== Traffic Keeper FPK Builder v${VERSION} ==="
command -v fnpack &> /dev/null || { echo "错误: fnpack 未安装"; exit 1; }
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/cmd" "${BUILD_DIR}/app/server" "${BUILD_DIR}/app/ui/images" "${BUILD_DIR}/config"
cp -r app/server/* "${BUILD_DIR}/app/server/"
cp -r app/ui/* "${BUILD_DIR}/app/ui/"
cp -r cmd/* "${BUILD_DIR}/cmd/"
cp -r config/* "${BUILD_DIR}/config/"
cp manifest "${BUILD_DIR}/"
cp ICON.PNG "${BUILD_DIR}/"
cp ICON_256.PNG "${BUILD_DIR}/"
chmod +x "${BUILD_DIR}/cmd/main" "${BUILD_DIR}/app/server/"*.sh
cd "${BUILD_DIR}" && fnpack build
OUTPUT="../traffic-keeper/traffic-keeper.fpk"
cp "${BUILD_DIR}/${APP_NAME}.fpk" "${OUTPUT}"
echo ""
echo "构建成功: ${OUTPUT} ($(du -h "${OUTPUT}" | cut -f1))"
