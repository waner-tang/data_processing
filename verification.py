import os


def get_all_files_with_relative_paths(root_dir):
    file_dict = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            file_dict[rel_path] = os.path.join(dirpath, filename)
    return file_dict


def find_duplicate_files(folder1, folder2):
    files1 = get_all_files_with_relative_paths(folder1)
    files2 = get_all_files_with_relative_paths(folder2)

    duplicates = set(files1.keys()) & set(files2.keys())

    return [(file, files1[file], files2[file]) for file in duplicates]


if __name__ == "__main__":
    folder1 = "data/h"  # 修改为你的文件夹路径
    folder2 = "data/hh"  # 修改为你的文件夹路径

    duplicate_files = find_duplicate_files(folder1, folder2)

    if duplicate_files:
        print("Duplicate files found:")
        for rel_path, path1, path2 in duplicate_files:
            print(f"{rel_path}\n  Folder1: {path1}\n  Folder2: {path2}\n")
    else:
        print("No duplicate files found.")