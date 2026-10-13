"""把下载文件夹里堆着的文件按类型自动归类。

用法::

    python clean_downloads.py              # 整理系统的「下载」文件夹 (~/Downloads)
    python clean_downloads.py D:\\some\\dir  # 整理指定文件夹

只移动文件，不会删除任何东西；遇到重名会自动加 -1、-2 后缀，不覆盖已有文件。
"""
import shutil
import sys
from pathlib import Path

# 文件类型分类规则
RULES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "文档": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "音乐": [".mp3", ".wav", ".flac", ".aac"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "程序": [".exe", ".msi", ".dmg", ".pkg"],
}

# 反过来建一张 后缀 -> 分类 的表，省掉每个文件都遍历一遍 RULES
SUFFIX_TO_FOLDER = {
    suffix: folder for folder, suffixes in RULES.items() for suffix in suffixes
}


def unique_path(target: Path) -> Path:
    """目标已存在时，自动找一个不重名的路径，避免把已有文件覆盖掉。"""
    if not target.exists():
        return target
    stem, suffix, n = target.stem, target.suffix, 1
    while True:
        candidate = target.with_name(f"{stem}-{n}{suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def organize(folder: Path) -> int:
    """把 folder 里的文件按类型分到子文件夹，返回移动的文件数。"""
    if not folder.is_dir():
        print(f"找不到文件夹: {folder}")
        return 0

    moved = 0
    # sorted() 让每次运行的处理顺序一致，输出可复现
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        target_folder = SUFFIX_TO_FOLDER.get(item.suffix.lower())
        if target_folder is None:
            continue
        target_dir = folder / target_folder
        target_dir.mkdir(exist_ok=True)
        destination = unique_path(target_dir / item.name)
        shutil.move(str(item), str(destination))
        print(f"移动: {item.name} -> {target_folder}/")
        moved += 1

    return moved


def main() -> None:
    folder = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Downloads"
    print(f"整理目录: {folder}")
    moved = organize(folder)
    print(f"\n整理完成！共移动 {moved} 个文件。")


if __name__ == "__main__":
    main()
