#!/usr/bin/env python3
"""
PaperForge 环境检查脚本
验证 GEE Python API 及其他依赖是否就绪
"""

import sys


def check_python():
    print(f"  ✅ Python: {sys.version.split()[0]}")
    return True


def check_ee():
    try:
        import ee
        print(f"  ✅ earthengine-api: {ee.__version__}")
        try:
            ee.Initialize()
            print(f"  ✅ GEE 认证: 已认证")
            return True
        except Exception as e:
            print(f"  ❌ GEE 认证: 未认证")
            print(f"     📋 请运行: earthengine authenticate")
            print(f"     或使用服务账号: ee.Initialize(project='...', credentials='...')")
            return False
    except ImportError:
        print(f"  ❌ earthengine-api: 未安装")
        print(f"     📋 请运行: pip install earthengine-api")
        return False
    except Exception as e:
        print(f"  ❌ earthengine-api error: {e}")
        return False


def check_geemap():
    try:
        import geemap
        print(f"  ✅ geemap: {geemap.__version__}")
        return True
    except ImportError:
        print(f"  ❌ geemap: 未安装")
        print(f"     📋 请运行: pip install geemap")
        return False


def check_deps():
    deps = {
        "pandas": "数据处理",
        "numpy": "数值计算",
        "matplotlib": "可视化",
        "requests": "网络请求",
        "seaborn": "统计图表"
    }
    all_ok = True
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep}: {desc}")
        except ImportError:
            print(f"  ❌ {dep}: 未安装 ({desc})")
            all_ok = False
    return all_ok


def check_proxy():
    import os
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy") or ""
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if http_proxy:
        print(f"  ℹ️  HTTP_PROXY: {http_proxy}")
    if https_proxy:
        print(f"  ℹ️  HTTPS_PROXY: {https_proxy}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PaperForge 环境检查")
    parser.add_argument("--project", help="GEE Project ID")
    args = parser.parse_args()
    
    print("🔨 PaperForge 环境检查")
    print("=" * 50)
    print()
    
    all_ok = True
    all_ok &= check_python()
    print()
    all_ok &= check_ee()
    print()
    all_ok &= check_geemap()
    print()
    all_ok &= check_deps()
    print()
    check_proxy()
    print()
    
    if args.project:
        print(f"  ℹ️  GEE Project: {args.project}")
    
    print()
    print("=" * 50)
    if all_ok:
        print("✅ 环境检查通过！可以运行 PaperForge 🚀")
    else:
        print("⚠️  部分依赖缺失，请按提示安装。")
    print()


if __name__ == "__main__":
    main()
