import os
import mimetypes
import pyperclip
import argparse
from datetime import datetime
import shutil
import colorama
from colorama import Fore, Style, Back
import json
import yaml
import fnmatch
from tqdm import tqdm
import zipfile

SKIP_FOLDERS = [
    # Version control
    ".git",
    ".svn",
    ".hg",
    ".bzr",
    # Dependencies and package managers
    "node_modules",
    "bower_components",
    "jspm_packages",
    "vendor",
    "packages",
    "composer.phar",
    # Python
    "venv",
    ".venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    "pip-wheel-metadata",
    ".eggs",
    "*.egg-info",
    # Build outputs
    "dist",
    "build",
    "out",
    "target",
    "bin",
    "obj",
    # IDE and editor specific
    ".idea",
    ".vscode",
    ".vs",
    "*.sublime-*",
    ".atom",
    ".eclipse",
    ".settings",
    # OS specific
    ".DS_Store",
    "Thumbs.db",
    # Logs and temporary files
    "logs",
    "*.log",
    "tmp",
    "temp",
    # Configuration and local settings
    ".env.local",
    ".env.*.local",
    # Docker
    ".docker",
    # Coverage reports
    "coverage",
    ".coverage",
    "htmlcov",
    # Documentation builds
    "docs/_build",
    "site",
    # Compiled source
    "*.com",
    "*.class",
    "*.dll",
    "*.exe",
    "*.o",
    "*.so",
]

TREE_ONLY_SKIP_FOLDERS = [
    "node_modules",
    "bower_components",
    "jspm_packages",
    "vendor",
    "packages",
    "composer.phar",
    "venv",
    ".venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    "pip-wheel-metadata",
    ".eggs",
    "*.egg-info",
    "dist",
    "build",
    "out",
    "target",
    "bin",
    "obj",
    ".idea",
    ".vscode",
    ".vs",
    "*.sublime-*",
    ".atom",
    ".eclipse",
    ".settings",
    ".DS_Store",
    "Thumbs.db",
    "logs",
    "*.log",
    "tmp",
    "temp",
    ".env.local",
    ".env.*.local",
    ".docker",
    "coverage",
    ".coverage",
    "htmlcov",
    "docs/_build",
    "site",
    "*.com",
    "*.class",
    "*.dll",
    "*.exe",
    "*.o",
    "*.so",
]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB

def get_pit_folder():
    return os.path.join(os.path.expanduser("~"), ".pit")

def load_gitignore(path):
    gitignore_patterns = []
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            gitignore_patterns = [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    return gitignore_patterns

def should_skip(path, skip_patterns, gitignore_patterns):
    relative_path = os.path.relpath(path)
    if any(
        fnmatch.fnmatch(relative_path, pattern)
        for pattern in skip_patterns + gitignore_patterns
    ):
        return True
    return False

def get_file_metadata(file_path):
    stats = os.stat(file_path)
    return {
        "size": stats.st_size,
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "permissions": oct(stats.st_mode)[-3:],
    }

def get_file_content(
    file_path, output_dir, relative_path, single_file=False, include_content=True
):
    if not include_content:
        return get_file_metadata(file_path)

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE and not single_file:
        return handle_large_file(file_path, output_dir, relative_path)

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type and mime_type.startswith("text"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return {**get_file_metadata(file_path), "content": content}
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="iso-8859-1") as file:
                    content = file.read()
                return {**get_file_metadata(file_path), "content": content}
            except Exception:
                return {
                    **get_file_metadata(file_path),
                    "content": f"[Unable to read {os.path.basename(file_path)}]",
                }
    else:
        return {
            **get_file_metadata(file_path),
            "content": f"[{os.path.splitext(file_path)[1]} file]",
        }

def handle_large_file(file_path, output_dir, relative_path):
    file_name = os.path.basename(file_path)
    parts_dir = os.path.join(output_dir, f"{file_name}_parts")
    os.makedirs(parts_dir, exist_ok=True)
    part_num = 1
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            part_file = os.path.join(parts_dir, f"{file_name}.part{part_num}")
            with open(part_file, "wb") as part:
                part.write(chunk)
            part_num += 1

    return {
        **get_file_metadata(file_path),
        "content": f"[Large file split into {part_num - 1} parts. See {os.path.relpath(parts_dir, output_dir)}]",
    }

def generate_content(
    path,
    output_dir,
    skip_patterns,
    gitignore_patterns,
    tree_only=False,
    single_file=False,
    include_content=True,
):
    content = {}
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        if should_skip(item_path, skip_patterns, gitignore_patterns):
            continue
        if os.path.isdir(item_path):
            content[item] = generate_content(
                item_path,
                output_dir,
                skip_patterns,
                gitignore_patterns,
                tree_only,
                single_file,
                include_content,
            )
        else:
            if tree_only:
                content[item] = None
            else:
                content[item] = get_file_content(
                    item_path, output_dir, item, single_file, include_content
                )
    return content

def content_to_markdown(content, indent=""):
    md_content = []
    for key, value in content.items():
        if value is None or isinstance(value, dict) and "content" not in value:
            md_content.append(f"{indent}- {key}/")
            if value:
                md_content.extend(content_to_markdown(value, indent + "  "))
        else:
            md_content.append(f"{indent}- {key}")
            if isinstance(value, dict) and "content" in value:
                md_content.append(f"{indent}  ```")
                md_content.append(f"{indent}  {value['content']}")
                md_content.append(f"{indent}  ```")
    return md_content

def compress_output(output_dir, compressed_file):
    with zipfile.ZipFile(compressed_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), output_dir),
                )

def print_styled_header(text):
    print(f"\n{Back.CYAN}{Fore.BLACK}{text:^50}{Style.RESET_ALL}")

def print_styled_section(title, content):
    print(f"\n{Fore.CYAN}{title}:")
    for line in content:
        print(f"   {line}")

def make_clickable(path):
    return f"\033]8;;file://{path}\033\\{path}\033]8;;\033\\"

def list_directory(path):
    print(f"\n{Fore.CYAN}Contents of {Fore.YELLOW}{path}{Fore.RESET}:")
    for item in sorted(os.listdir(path)):
        if os.path.isdir(os.path.join(path, item)):
            print(f"  {Fore.BLUE}📁 {item}/{Fore.RESET}")
        else:
            print(f"  {Fore.GREEN}📄 {item}{Fore.RESET}")
    print()

def purge_data():
    pit_folder = get_pit_folder()

    if os.path.exists(pit_folder):
        try:
            shutil.rmtree(pit_folder)
            print(
                f"{Fore.GREEN}✅ Successfully purged all PackItUp data from {pit_folder}"
            )
        except Exception as e:
            print(f"{Fore.RED}❌ Error while purging data: {e}")
    else:
        print(f"{Fore.YELLOW}⚠️ No PackItUp data found to purge.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="PackItUp: A tool for packaging files and directories."
    )
    parser.add_argument("path", help="Path to the directory or file to process.")
    parser.add_argument(
        "-t",
        "--type",
        choices=["tree", "archive"],
        default="tree",
        help="Output type: 'tree' for directory structure or 'archive' for zip.",
    )
    parser.add_argument(
        "-p",
        "--purge",
        action="store_true",
        help="Purge existing PackItUp data.",
    )
    parser.add_argument(
        "-s",
        "--single",
        action="store_true",
        help="Process a single file instead of directories.",
    )
    parser.add_argument(
        "-c",
        "--no-content",
        action="store_true",
        help="Exclude file contents from the output.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path to save the output file or directory.",
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    pit_folder = get_pit_folder()

    if args.purge:
        purge_data()
        return

    if args.type == "archive":
        if args.output is None:
            args.output = os.path.join(pit_folder, "output.zip")

        print_styled_header("Packing Files into Archive")

        content = generate_content(
            args.path,
            pit_folder,
            SKIP_FOLDERS,
            load_gitignore(args.path),
            single_file=args.single,
            include_content=not args.no_content,
        )

        compressed_file = args.output
        compress_output(pit_folder, compressed_file)

        print_styled_section(
            "Archive Created", [f"File: {make_clickable(compressed_file)}"]
        )

    elif args.type == "tree":
        if args.output is None:
            args.output = os.path.join(pit_folder, "tree.md")

        print_styled_header("Generating Directory Tree")

        content = generate_content(
            args.path,
            pit_folder,
            TREE_ONLY_SKIP_FOLDERS,
            load_gitignore(args.path),
            tree_only=True,
            single_file=args.single,
            include_content=False,
        )

        md_content = content_to_markdown(content)
        with open(args.output, "w") as f:
            f.write("\n".join(md_content))

        print_styled_section(
            "Tree Generated", [f"File: {make_clickable(args.output)}"]
        )

if __name__ == "__main__":
    colorama.init()
    main()
