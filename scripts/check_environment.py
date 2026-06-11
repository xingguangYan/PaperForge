#!/usr/bin/env python3
"""
GeoRS-Pipeline 环境检查脚本
验证 GEE Python API 环境是否就绪
"""

import subprocess
import sys


def check_python():
    print(f"  Python: {sys.version}")
    return True


def check_ee():
    try:
        import ee
        print("  earthengine-api: 已安装")
        try:
            ee.Initialize()
            print("  GEE 认证: ✓ 已认证")
            return True
        except Exception as e:
            print(f"  GEE 认证: ✗ 未认证 ({e})")
            print("    请运行: earthengine authenticate")
            return False
    except ImportError:
        print("  earthengine-api: ✗ 未安装")
        print("    请运行: pip install earthengine-api")
        return False


def check_geemap():
    try:
        import geemap
        print(f"  geemap: ✓ 已安装 (v{geemap.__version__})")
        return True
    except ImportError:
        print("  geemap: ✗ 未安装")
        print("    请运行: pip install geemap")
        return False


def check_deps():
    deps = ["pandas", "numpy", "matplotlib", "requests"]
    for dep in deps:
        try:
            __import__(dep)
            print(f"  {dep}: ✓")
        except ImportError:
            print(f"  {dep}: ✗ 未安装")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="GeoRS-Pipeline 环境检查")
    parser.add_argument("--project", help="GEE Project ID")
    args = parser.parse_args()

    print("GeoRS-Pipeline 环境检查")
    print("=" * 40)

    check_python()
    print()
    check_ee()
    print()
    check_geemap()
    print()
    check_deps()
    print()

    if args.project:
        print(f"  Project ID: {args.project}")

    print("\n" + "=" * 40)
    print("检查完成")


if __name__ == "__main__":
    main()
