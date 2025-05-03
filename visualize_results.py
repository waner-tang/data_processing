import os
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal


def process_line(line):
    """
    处理单行数据，保证顺序为：x, y, z, nx, ny, nz, label。
    同时对法向量进行归一化处理。
    """
    columns = line.split()  # 假设数据以空格或制表符分隔
    if len(columns) == 7:
        x, y, z, nx, ny, nz, label = columns
        normals = np.array([nx, ny, nz], dtype=np.float64)
        # 检查是否有 NaN 或 Inf
        if np.isnan(normals).any():
            print("has_nan: True")
            return None
        if np.isinf(normals).any():
            print("has_inf: True")
            return None
        # 归一化法向量
        norm_val = np.linalg.norm(normals)
        if norm_val == 0:
            print("Zero norm encountered, skipping normalization.")
            return None  # 或者对零向量做特殊处理
        normalized_normals = normals / norm_val
        normalized_normals = np.round(normalized_normals, decimals=8)
        nx, ny, nz = normalized_normals
        # 使用 Decimal 保持精度
        new_line = f"{Decimal(x)} {Decimal(y)} {Decimal(z)} {nx} {ny} {nz} {Decimal(float(label)):.6f}\n"
        return new_line
    else:
        print("errors!!")
        return None


def process_file_txt(input_file_path, processed_file_path):
    """
    对单个 txt 文件做预处理（例如处理法向量归一化等），
    将处理后的数据写入 processed_file_path。
    """
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()
    new_lines = [process_line(line) for line in lines]
    # 过滤掉处理失败的行
    new_lines = [line for line in new_lines if line is not None]
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
    with open(processed_file_path, 'w') as outfile:
        outfile.writelines(new_lines)
    return processed_file_path


def load_point_cloud(file_path):
    """
    加载点云数据，返回 numpy 数组，数据类型为 float。
    假定每行数据格式为：x y z nx ny nz label
    """
    data = np.loadtxt(file_path)
    if data.ndim == 1:
        # 只有一行数据
        data = data.reshape(1, -1)
    return data


def visualize_point_cloud(data, output_image_path):
    """
    可视化点云：
      - 左图显示 y > 0 的点（从 +Y 投影到 xz 平面）
      - 中图显示 y <= 0 的点（从 -Y 投影到 xz 平面）
      - 右图显示 x <= 0 的点（从 +X 投影到 yz 平面）
      - 标签为3的点放大显示
    """
    # 提取字段
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    labels = data[:, 6]

    # 掩码定义
    mask_pos_y = y > 0
    mask_neg_y = y <= 0
    mask_neg_x = x <= 0

    def get_plot_data(mask, axis1, axis2):
        axis1_vals = axis1[mask]
        axis2_vals = axis2[mask]
        labels_sub = labels[mask]

        # 点大小
        sizes = np.full_like(labels_sub, 1, dtype=float)
        # sizes[labels_sub == 3] = 5

        # 点颜色
        colors = np.empty(labels_sub.shape, dtype=object)
        colors[labels_sub == 1] = 'blue'
        colors[labels_sub == 2] = 'green'
        colors[labels_sub == 3] = 'red'

        # 点透明度
        alphas = np.full_like(labels_sub, 0.3, dtype=float)  # 默认较透明
        # alphas[labels_sub == 3] = 1.0  # 标签为3的不透明

        return axis1_vals, axis2_vals, sizes, colors, alphas

    # 获取每个图的数据
    x1, z1, sizes1, colors1, alphas1 = get_plot_data(mask_pos_y, x, z)
    x2, z2, sizes2, colors2, alphas2 = get_plot_data(mask_neg_y, x, z)
    y3, z3, sizes3, colors3, alphas3 = get_plot_data(mask_neg_x, y, z)
    # 开始绘图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # 3列

    # 图 1：Y > 0
    axes[0].scatter(x1, z1, s=sizes1, c=colors1, alpha=alphas1)
    axes[0].set_title("Y > 0 (Projection to XZ)")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Z")
    axes[0].grid(True)
    axes[0].set_aspect('equal')

    # 图 2：Y <= 0
    axes[1].scatter(x2, z2, s=sizes2, c=colors2, alpha=alphas2)
    axes[1].set_title("Y <= 0 (Projection to XZ)")
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Z")
    axes[1].grid(True)
    axes[1].set_aspect('equal')

    # 图 3：X <= 0
    axes[2].scatter(y3, z3, s=sizes3, c=colors3, alpha=alphas3)
    axes[2].set_title("X <= 0 (Projection to YZ)")
    axes[2].set_xlabel("Y")
    axes[2].set_ylabel("Z")
    axes[2].grid(True)
    axes[2].set_aspect('equal')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    plt.savefig(output_image_path, dpi=600)
    plt.close(fig)
    print(f"Saved visualization to {output_image_path}")


def process_directory(input_dir, processed_dir, output_image_dir):
    """
    递归遍历 input_dir 中所有 txt 文件：
      1. 对每个 txt 文件预处理（归一化法向量）
      2. 加载处理后的点云数据并可视化保存为 jpg
    对应的输出文件会放到 processed_dir（处理后的 txt 文件）和 output_image_dir（jpg文件），
    同时保持相对目录结构。
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)

                # 生成预处理 txt 文件路径
                relative_path = os.path.relpath(input_file_path, input_dir)
                processed_file_path = os.path.join(processed_dir, relative_path)

                # 生成输出图片的路径，扩展名改为 jpg
                output_image_path = os.path.join(output_image_dir, os.path.splitext(relative_path)[0] + ".jpg")

                print(f"Processing file: {input_file_path}")
                # 对 txt 文件进行预处理
                proc_file = process_file_txt(input_file_path, processed_file_path)
                # 加载点云数据
                try:
                    data = load_point_cloud(proc_file)
                except Exception as e:
                    print(f"Error loading {proc_file}: {e}")
                    continue
                # 对点云数据进行可视化，并保存 jpg
                visualize_point_cloud(data, output_image_path)


if __name__ == "__main__":
    # 输入包含原始 txt 文件的根目录（可包含嵌套子文件夹）
    input_directory = "data/24040209-M1-problems"
    # 预处理后的 txt 文件保存目录（你可以选择是否保留预处理结果）
    processed_directory = "data_output/24040209-M1-problems/processed_txt"
    # 可视化图片保存的目录（jpg 格式）
    output_image_directory = "data_output/24040209-M1-problems/output_images"

    process_directory(input_directory, processed_directory, output_image_directory)
    print("所有文件处理并可视化完成！")