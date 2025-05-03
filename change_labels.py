import os
from decimal import Decimal

def process_line(line):
    """处理每行数据，调整顺序：x/y/z 法向量 x/y/z 标签，
       并在映射标签后保留原有小数位数。"""
    columns = line.split()
    if len(columns) == 7:
        x_str, y_str, z_str, nx_str, ny_str, nz_str, label_str = columns

        # 坐标和法向量使用 Decimal 保留原有小数位
        x  = Decimal(x_str)
        y  = Decimal(y_str)
        z  = Decimal(z_str)
        nx = Decimal(nx_str)
        ny = Decimal(ny_str)
        nz = Decimal(nz_str)

        # 原标签 Decimal，用于量化
        label_dec = Decimal(label_str)

        # 标签映射：1、2 -> 0；3 -> 1；其他保持不变
        orig_int = int(label_dec)
        if orig_int in (1, 2):
            mapped = 0
        elif orig_int == 3:
            mapped = 1
        else:
            mapped = orig_int

        # 按原标签的小数位数量化映射结果
        new_label = Decimal(mapped).quantize(label_dec)

        # 拼成新行
        new_line = (
            f"{x} {y} {z} "
            f"{nx} {ny} {nz} "
            f"{new_label}\n"
        )
        return new_line
    else:
        print("columns != 7:", line.strip())
        return line

def process_file(file_path, output_file_path):
    with open(file_path, 'r') as infile:
        lines = infile.readlines()
    new_lines = [process_line(l) for l in lines]
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(new_lines)

def process_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.txt'):
                in_path  = os.path.join(root, f)
                rel_path = os.path.relpath(in_path, input_dir)
                out_path = os.path.join(output_dir, rel_path)
                process_file(in_path, out_path)

if __name__ == "__main__":
    input_directory  = "data/test_set"
    output_directory = "data_output/test_set"
    process_directory(input_directory, output_directory)
    print("处理完成！")
