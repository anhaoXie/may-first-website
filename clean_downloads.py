import os
import shutil
from pathlib import Path

# 你的下载文件夹路径，改成你自己的
DOWNLOADS = Path(r"D:\my first website")

# 文件类型分类规则
RULES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "文档": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "音乐": [".mp3", ".wav", ".flac", ".aac"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "程序": [".exe", ".msi", ".dmg", ".pkg"],
}


def organize():
    if not DOWNLOADS.exists():
        print(f"找不到文件夹: {DOWNLOADS}")
        return

    moved = 0
    for file in DOWNLOADS.iterdir():
        if file.is_file():
            suffix = file.suffix.lower()
            for folder, extensions in RULES.items():
                if suffix in extensions:
                    target_dir = DOWNLOADS / folder
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))
                    print(f"移动: {file.name} -> {folder}/")
                    moved += 1
                    break

    print(f"\n整理完成！共移动 {moved} 个文件。")


if __name__ == "__main__":
    organize()