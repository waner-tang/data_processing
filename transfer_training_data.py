import os
from decimal import Decimal


def process_line(line):
    """处理每行数据，调整顺序：x/y/z 法向量 x/y/z 标签"""
    columns = line.split()  # 假设数据以空格或制表符分隔
    if len(columns) == 7:
        # 提取各列数据
        x, y, z, nx, ny, nz, label = columns
        # 使用Decimal来保持精度并重新排列
        new_line = f"{Decimal(x)} {Decimal(y)} {Decimal(z)} {Decimal(nx)} {Decimal(ny)} {Decimal(nz)}\n"
        return new_line
    else:
        # 如果不是7列数据，直接返回原始行
        print("columns != 7")
        return line


def process_file(file_path, output_file_path):
    """处理单个文件，调整数据顺序并保存到新的文件中"""
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # 调整每行的顺序
    new_lines = [process_line(line) for line in lines]

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

                # 处理文件名：如果以 _predicted 结尾，则去掉它
                file_name, ext = os.path.splitext(relative_path)
                if file_name.endswith('_predicted'):
                    file_name = file_name[:-10]  # 去掉 "_predicted"
                output_file_path = os.path.join(output_dir, file_name + ext)

                # 处理每个文件
                process_file(input_file_path, output_file_path)


if __name__ == "__main__":
    input_directory = "data"  # 输入文件夹路径
    output_directory = "data_output/test"  # 输出文件夹路径

    # 处理文件夹
    process_directory(input_directory, output_directory)

    print("处理完成！")
