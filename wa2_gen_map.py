#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
字符映射表生成器
用于生成从A文本文件到B文本文件的字符映射表
"""

import argparse
import json
import os


def create_character_mapping(file_a_path, file_b_path, output_path, format_type="json"):
    """
    创建从文件A到文件B的字符映射表并输出到文件

    Args:
        file_a_path: 源文件A路径
        file_b_path: 目标文件B路径
        output_path: 输出映射表文件路径
        format_type: 输出格式(json, python)
    """
    # 读取文件内容
    try:
        with open(file_a_path, "r", encoding="utf-8") as file_a:
            content_a = file_a.read()

        with open(file_b_path, "r", encoding="utf-8") as file_b:
            content_b = file_b.read()
    except Exception as e:
        print(f"读取文件错误: {e}")
        return False

    # 检查文件长度，如果不同则给出警告
    if len(content_a) != len(content_b):
        print(
            f"警告：文件长度不匹配。文件A: {len(content_a)}字符，文件B: {len(content_b)}字符"
        )
        print("将只映射A中存在且在B长度范围内的字符")

    # 创建映射字典
    char_map = {}
    conflict_chars = {}

    # 确定要处理的最大长度
    max_length = min(len(content_a), len(content_b))

    for i in range(max_length):
        char_a = content_a[i]
        char_b = content_b[i]

        # 跳过换行符
        if char_a == "\n":
            continue
        if char_b == "\n":
            continue

        # 处理映射冲突
        if char_a in char_map and char_map[char_a] != char_b:
            if char_a not in conflict_chars:
                conflict_chars[char_a] = set([char_map[char_a]])
            conflict_chars[char_a].add(char_b)
            continue

        char_map[char_a] = char_b

    # 显示冲突信息
    if conflict_chars:
        print("警告：检测到字符映射冲突:")
        for char, mappings in conflict_chars.items():
            print(f"  '{char}' -> {mappings}")

    # 输出映射到文件
    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
            if format_type == "json":
                json.dump(char_map, output_file, ensure_ascii=False, indent=2)
            elif format_type == "python":
                output_file.write("# 字符映射表\n")
                output_file.write("char_map = {\n")
                for char_a, char_b in sorted(char_map.items()):
                    char_a_escaped = repr(char_a)[1:-1]
                    char_b_escaped = repr(char_b)[1:-1]
                    output_file.write(f'    "{char_a_escaped}": "{char_b_escaped}",\n')
                output_file.write("}\n")

        print(f"映射表已成功写入到 {output_path}")
        print(f"共有 {len(char_map)} 个字符映射")
        return True
    except Exception as e:
        print(f"写入文件错误: {e}")
        return False


def main():
    """处理命令行参数并执行映射生成"""
    parser = argparse.ArgumentParser(description="创建从文件A到文件B的字符映射表")
    parser.add_argument("file_a", help="源文件A的路径")
    parser.add_argument("file_b", help="目标文件B的路径")
    parser.add_argument(
        "-o", "--output", help="输出文件路径", default="char_mapping.json"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "python"],
        default="json",
        help="输出格式：json 或 python (默认: json)",
    )

    args = parser.parse_args()

    create_character_mapping(args.file_a, args.file_b, args.output, args.format)


if __name__ == "__main__":
    main()
