#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找两个文件夹中重复的文件名
"""

import os
import sys
from pathlib import Path


def get_filenames_from_folder(folder_path):
    """
    获取指定文件夹中所有文件的文件名（不包括子文件夹）
    
    Args:
        folder_path (str): 文件夹路径
        
    Returns:
        set: 包含所有文件名的集合
    """
    try:
        folder = Path(folder_path)
        if not folder.exists():
            print(f"错误: 文件夹 '{folder_path}' 不存在")
            return set()
        
        if not folder.is_dir():
            print(f"错误: '{folder_path}' 不是一个文件夹")
            return set()
        
        # 获取所有文件名（不包括子文件夹）
        filenames = set()
        for item in folder.iterdir():
            if item.is_file():
                filenames.add(item.name)
        
        return filenames
    
    except Exception as e:
        print(f"读取文件夹 '{folder_path}' 时出错: {e}")
        return set()


def get_filenames_recursive(folder_path):
    """
    递归获取指定文件夹及其子文件夹中所有文件的文件名
    
    Args:
        folder_path (str): 文件夹路径
        
    Returns:
        set: 包含所有文件名的集合
    """
    try:
        folder = Path(folder_path)
        if not folder.exists():
            print(f"错误: 文件夹 '{folder_path}' 不存在")
            return set()
        
        if not folder.is_dir():
            print(f"错误: '{folder_path}' 不是一个文件夹")
            return set()
        
        # 递归获取所有文件名
        filenames = set()
        for item in folder.rglob('*'):
            if item.is_file():
                filenames.add(item.name)
        
        return filenames
    
    except Exception as e:
        print(f"读取文件夹 '{folder_path}' 时出错: {e}")
        return set()


def find_duplicate_filenames(folder1_path, folder2_path, recursive=False):
    """
    查找两个文件夹中重复的文件名
    
    Args:
        folder1_path (str): 第一个文件夹路径
        folder2_path (str): 第二个文件夹路径
        recursive (bool): 是否递归搜索子文件夹，默认为False
        
    Returns:
        set: 重复的文件名集合
    """
    print(f"正在扫描文件夹: {folder1_path}")
    if recursive:
        filenames1 = get_filenames_recursive(folder1_path)
    else:
        filenames1 = get_filenames_from_folder(folder1_path)
    
    print(f"正在扫描文件夹: {folder2_path}")
    if recursive:
        filenames2 = get_filenames_recursive(folder2_path)
    else:
        filenames2 = get_filenames_from_folder(folder2_path)
    
    # 找出重复的文件名
    duplicate_filenames = filenames1.intersection(filenames2)
    
    return duplicate_filenames, len(filenames1), len(filenames2)


def main():
    """主函数"""
    print("=" * 50)
    print("查找两个文件夹中重复的文件名")
    print("=" * 50)
    
    # 获取用户输入
    if len(sys.argv) >= 3:
        folder1 = sys.argv[1]
        folder2 = sys.argv[2]
        recursive = len(sys.argv) > 3 and sys.argv[3].lower() in ['true', '1', 'yes', 'recursive']
    else:
        folder1 = input("请输入第一个文件夹路径: ").strip()
        folder2 = input("请输入第二个文件夹路径: ").strip()
        recursive_input = input("是否递归搜索子文件夹? (y/n, 默认n): ").strip().lower()
        recursive = recursive_input in ['y', 'yes', 'true', '1']
    
    if not folder1 or not folder2:
        print("错误: 请提供两个有效的文件夹路径")
        return
    
    print(f"\n搜索模式: {'递归搜索（包括子文件夹）' if recursive else '仅搜索当前文件夹'}")
    print("-" * 50)
    
    # 查找重复文件名
    duplicate_filenames, count1, count2 = find_duplicate_filenames(folder1, folder2, recursive)
    
    # 输出结果
    print(f"\n文件夹1 ({folder1}) 包含 {count1} 个文件")
    print(f"文件夹2 ({folder2}) 包含 {count2} 个文件")
    print("-" * 50)
    
    if duplicate_filenames:
        print(f"\n找到 {len(duplicate_filenames)} 个重复的文件名:")
        print("-" * 30)
        for filename in sorted(duplicate_filenames):
            print(f"  • {filename}")
    else:
        print("\n没有找到重复的文件名")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main() 