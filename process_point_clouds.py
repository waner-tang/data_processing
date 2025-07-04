import os
from decimal import Decimal


def process_line(line):
    """处理每行数据，交换标签1和标签2"""
    columns = line.strip().split()  # 假设数据以空格或制表符分隔
    if len(columns) == 7:
        # 提取各列数据
        x, y, z, nx, ny, nz, label = columns
        
        # 交换标签1和标签2
        if label == "1":
            new_label = "2"
        elif label == "2":
            new_label = "1"
        else:
            new_label = label  # 其他标签保持不变
            
        # 使用Decimal来保持精度并返回处理后的行
        new_line = f"{Decimal(x)} {Decimal(y)} {Decimal(z)} {Decimal(nx)} {Decimal(ny)} {Decimal(nz)} {new_label}"
        return new_line
    else:
        # 如果不是7列数据，输出警告并返回原始行
        print(f"警告：发现非7列数据: {line}")
        return line.strip()


def process_file(file_path, output_dir):
    """处理单个文件，交换标签并按标签分类保存"""
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # 处理每行数据
    processed_lines = [process_line(line) for line in lines]
    
    # 按标签分组
    label_groups = {
        "1": [],  # C类
        "2": [],  # P类
        "3": []   # S类
    }
    
    for line in processed_lines:
        columns = line.split()
        if len(columns) == 7:
            label = columns[6]
            if label in label_groups:
                label_groups[label].append(line)
            else:
                print(f"警告：未知标签 {label}")
    
    # 获取原始文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 为每个标签创建对应的输出文件
    label_suffixes = {
        "1": "-C",
        "2": "-P",
        "3": "-S"
    }
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存每个标签的点云到单独的文件
    for label, lines in label_groups.items():
        if lines:  # 只有当有数据时才创建文件
            suffix = label_suffixes.get(label, f"-{label}")
            output_file_path = os.path.join(output_dir, f"{base_name}{suffix}.txt")
            with open(output_file_path, 'w') as outfile:
                outfile.write('\n'.join(lines) + '\n')


def process_directory(input_dir, output_dir):
    """递归遍历输入文件夹并处理所有txt文件"""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)
                
                # 保持相对路径结构
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                
                # 确保输出子目录存在
                os.makedirs(output_subdir, exist_ok=True)
                
                # 处理每个文件
                process_file(input_file_path, output_subdir)


if __name__ == "__main__":
    input_directory = input("请输入源文件夹路径: ")
    output_directory = input("请输入目标文件夹路径: ")
    
    # 处理文件夹
    process_directory(input_directory, output_directory)
    
    print("处理完成！") 