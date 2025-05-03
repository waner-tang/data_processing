import os
from decimal import Decimal
import numpy as np


def process_line(line):
    """处理每行数据，调整顺序：x/y/z 法向量 x/y/z 标签"""
    columns = line.split()  # 假设数据以空格或制表符分隔
    if len(columns) == 7:
        # 提取各列数据
        x, y, z, label, nx, ny, nz = columns
        normals = np.array([nx, ny, nz], dtype=np.float64)  # shape: (3,)

        # 检查是否有 NaN
        has_nan = np.isnan(normals).any()
        if has_nan:
            print(" has_nan:true")
            return None

        # 检查是否有 Inf
        has_inf = np.isinf(normals).any()
        if has_inf:
            print("has_inf:true")
            return None

        norms = np.linalg.norm(normals)  # 计算标量模

        # 检查模是否为零
        if norms == 0:
            print("Warning: Zero-length normal vector detected.")
            return None  # 如果模为零，跳过该行

        # 归一化法向量
        normalized_normals = normals / norms  # 直接除以标量
        normalized_normals = np.round(normalized_normals, decimals=8)
        nx, ny, nz = normalized_normals

        # 使用Decimal来保持精度并重新排列
        new_line = f"{Decimal(x)} {Decimal(y)} {Decimal(z)} {nx} {ny} {nz} {Decimal(float(label)):.6f}\n"
        return new_line
    else:
        # 如果不是7列数据，直接返回原始行
        print("errors!!")
        return None


def process_file(file_path, output_file_path):
    """处理单个文件，调整数据顺序并保存到新的文件中"""
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # 调整每行的顺序
    new_lines = [process_line(line) for line in lines]

    # 过滤掉返回 None 的行（即包含 NaN 或 Inf 的行）
    new_lines = [line for line in new_lines if line is not None]

    # 创建输出文件夹，如果不存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # 将调整后的数据保存到新文件
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(new_lines)


def process_directory(input_dir, output_dir):
    """递归遍历输入文件夹并处理所有txt文件"""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)

                # 处理每个文件
                process_file(input_file_path, output_file_path)


if __name__ == "__main__":
    input_directory = "data/test/JA1ES24020211-M1"  # 输入文件夹路径
    output_directory = "data_output/test/JA1ES24020211-M1"  # 输出文件夹路径

    # 处理文件夹
    process_directory(input_directory, output_directory)

    print("处理完成！")
