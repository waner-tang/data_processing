import os
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
from stl import mesh


def normalize_vector(vec):
    """归一化法向量"""
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec  # 如果法向量为零向量，直接返回原值
    return vec / norm


def process_stl_file(file_path, output_file_path):
    """处理单个STL文件，提取点云数据和法向量，保存为TXT格式"""
    # 读取STL文件
    stl_mesh = mesh.Mesh.from_file(file_path)

    # 提取点云数据和法向量
    vertices = stl_mesh.vectors  # 三角形的顶点坐标
    normals = stl_mesh.normals  # 面法向量

    # 创建一个字典，存储每个顶点的法向量
    vertex_normals = {tuple(v): [] for v in np.unique(vertices.reshape(-1, 3), axis=0)}  # 存储顶点法向量

    # 准备输出数据
    output_data = []

    # 遍历每个三角形，计算法向量，并更新每个顶点的法向量
    for i in range(len(vertices)):
        # 计算每个三角形的面法向量
        face_normal = normals[i]

        # 获取该三角形的三个顶点
        for j in range(3):
            x, y, z = vertices[i][j]
            nx, ny, nz = face_normal

            # 将当前面法向量添加到该顶点的法向量列表
            vertex_normals[tuple(vertices[i][j])].append(face_normal)

    # 计算顶点法向量：对每个顶点的所有相邻面法向量进行平均
    for vertex, normal_list in vertex_normals.items():
        if normal_list:
            # 对所有法向量进行加权平均
            averaged_normal = np.mean(normal_list, axis=0)
            normalized_normal = normalize_vector(averaged_normal)

            x, y, z = vertex
            nx, ny, nz = normalized_normal

            # 转换为 float 再转换为 Decimal 来避免 TypeError
            x = Decimal(float(x)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            y = Decimal(float(y)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            z = Decimal(float(z)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            nx = Decimal(float(nx)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            ny = Decimal(float(ny)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
            nz = Decimal(float(nz)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)

            output_data.append(f"{x} {y} {z} {nx} {ny} {nz}\n")

    # 创建输出文件夹，如果不存在
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # 将提取的数据保存到TXT文件
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(output_data)


def process_directory(input_dir, output_dir):
    """递归遍历输入文件夹并处理所有STL文件，将数据输出为TXT文件"""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.stl'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path.replace('.stl', '.txt'))

                # 处理每个STL文件，并保存为TXT
                process_stl_file(input_file_path, output_file_path)




if __name__ == "__main__":
    input_directory = "data/extract_points"  # 输入文件夹路径
    output_directory = "data_output/extract_points"  # 输出文件夹路径

    # 处理文件夹
    process_directory(input_directory, output_directory)

    print("处理完成！")
