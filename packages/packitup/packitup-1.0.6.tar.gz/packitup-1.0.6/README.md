# PackItUp

## 📦 Project Structure Generator and Documentation Tool

PackItUp is a powerful and flexible command-line tool designed to generate comprehensive documentation of your project's structure. It creates a detailed overview of your project's files and directories, making it easier to understand, share, and maintain your codebase.

## 🌟 Features

- 🌳 Generate project structure in tree format
- 📄 Include file contents (optional)
- 📊 Provide file metadata (size, last modified date, permissions)
- 🎨 Multiple output formats (Markdown, JSON, YAML)
- 🧹 Respect .gitignore patterns
- 🚫 Customizable file/directory exclusions
- 📦 Compress output (optional)
- 📏 Customizable file size limits
- 📋 Automatic clipboard copy of output

## 🛠 Installation

PackItUp is available on PyPI and can be installed with pip:

```
pip install packitup
```

This will install PackItUp and all its dependencies.

## 🚀 Usage

After installation, you can use PackItUp directly from the command line:

```
packitup [OPTIONS] [PATH]
```

If no path is specified, PackItUp will use the current directory.

### 🎛 Options

- `-t, --tree`: Generate file tree only (no file contents)
- `-l, --list`: List files and directories in the specified directory
- `-s, --singlefile`: Ignore file splitting and return as a single file
- `-p, --purge`: Purge all saved PackItUp data
- `-f, --format {markdown,json,yaml}`: Output format (default: markdown)
- `-m, --max-size BYTES`: Maximum file size in bytes (default: 5MB)
- `-c, --compress`: Compress the output files
- `-e, --exclude PATTERN [PATTERN ...]`: Additional patterns to exclude
- `--no-content`: Exclude file contents, only include metadata

## 📚 Examples

### 1. Basic Usage

Generate a Markdown report of the current directory:

```
packitup
```

This will create a Markdown file with the project structure, including file contents (up to 5MB per file) and metadata.

### 2. Specify a Different Directory

Generate a report for a specific project:

```
packitup /path/to/your/project
```

### 3. Generate Only the File Tree

To get a quick overview without file contents:

```
packitup -t
```

### 4. Change Output Format

Generate a JSON report:

```
packitup -f json
```

Or a YAML report:

```
packitup -f yaml
```

### 5. Customize File Size Limit

Set the maximum file size to 10MB:

```
packitup -m 10000000
```

### 6. Exclude Specific Patterns

Exclude all .log and .tmp files:

```
packitup -e *.log *.tmp
```

### 7. Generate a Compressed Output

Create a zip file containing the report:

```
packitup -c
```

### 8. Exclude File Contents

Generate a report with only metadata, no file contents:

```
packitup --no-content
```
    # Project Structure

- __init__.py
  ```
  
  ```
- packitup.py
  ```
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

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB


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
    name = os.path.basename(path)
    if any(
        fnmatch.fnmatch(name, pattern) for pattern in skip_patterns + gitignore_patterns
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
    home_dir = os.path.expanduser("~")
    home_packitup_dir = os.path.join(home_dir, ".packitup")

    if os.path.exists(home_packitup_dir):
        try:
            shutil.rmtree(home_packitup_dir)
            print(
                f"{Fore.GREEN}✅ Successfully purged all PackItUp data from {home_packitup_dir}"
            )
        except Exception as e:
            print(f"{Fore.RED}❌ Error while purging data: {e}")
    else:
        print(f"{Fore.YELLOW}⚠️ No PackItUp data found to purge.")

    # Also remove any local output directories in the current working directory
    cwd = os.getcwd()
    for item in os.listdir(cwd):
        if os.path.isdir(item) and item.endswith("_structure_"):
            try:
                shutil.rmtree(item)
                print(f"{Fore.GREEN}✅ Removed local output directory: {item}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error while removing {item}: {e}")


def main():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(
        description="Generate project structure and contents."
    )
    parser.add_argument(
        "path", nargs="?", default=".", help="Path to pack (default: current directory)"
    )
    parser.add_argument(
        "-t",
        "--tree",
        action="store_true",
        help="Generate file tree only (no file contents)",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List files and directories in the specified directory",
    )
    parser.add_argument(
        "-s",
        "--singlefile",
        action="store_true",
        help="Ignore file splitting and return as a single file",
    )
    parser.add_argument(
        "-p", "--purge", action="store_true", help="Purge all saved PackItUp data"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["markdown", "json", "yaml"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "-m", "--max-size", type=int, help="Maximum file size in bytes (default: 5MB)"
    )
    parser.add_argument(
        "-c", "--compress", action="store_true", help="Compress the output files"
    )
    parser.add_argument(
        "-e", "--exclude", nargs="+", help="Additional patterns to exclude"
    )
    parser.add_argument(
        "--no-content",
        action="store_true",
        help="Exclude file contents, only include metadata",
    )
    args = parser.parse_args()

    if args.purge:
        purge_data()
        return

    if args.max_size:
        global MAX_FILE_SIZE
        MAX_FILE_SIZE = args.max_size

    root_dir = os.path.abspath(args.path)

    if args.list:
        list_directory(root_dir)
        return

    gitignore_patterns = load_gitignore(root_dir)
    skip_patterns = SKIP_FOLDERS + (args.exclude or [])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    root_folder_name = os.path.basename(root_dir)

    output_dir = f"{root_folder_name}_structure_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(
        output_dir, f"{root_folder_name}_structure_{timestamp}.{args.format}"
    )

    print(f"Generating project structure for {root_dir}...")
    content = generate_content(
        root_dir,
        output_dir,
        skip_patterns,
        gitignore_patterns,
        args.tree,
        args.singlefile,
        not args.no_content,
    )

    if args.format == "markdown":
        output_content = "\n".join(
            ["# Project Structure", ""] + content_to_markdown(content)
        )
    elif args.format == "json":
        output_content = json.dumps(content, indent=2)
    else:  # yaml
        output_content = yaml.dump(content, default_flow_style=False)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_content)

    if args.compress:
        compressed_file = f"{output_file}.zip"
        print(f"Compressing output to {compressed_file}...")
        compress_output(output_dir, compressed_file)
        print(f"Compressed file saved to {compressed_file}")

    pyperclip.copy(output_content)

    print_styled_header("PackItUp Completed Successfully!")

    print_styled_section(
        "📁 Output Location",
        [f"📌 Local: {Fore.YELLOW}{make_clickable(os.path.abspath(output_dir))}"],
    )

    print_styled_section(
        "📄 Main File",
        [f"📌 Local: {Fore.YELLOW}{make_clickable(os.path.abspath(output_file))}"],
    )

    print_styled_section(
        "ℹ️  Info",
        [
            f"📋 Content has been copied to clipboard.",
            f"📂 Large files have been split and saved in parts if necessary.",
            f"🗂️  Skipped patterns: {', '.join(skip_patterns + gitignore_patterns)}",
        ],
    )


if __name__ == "__main__":
    main()

  ```
### 9. Combine Multiple Options

Generate a compressed JSON report with a 10MB file size limit, excluding .log files and file contents:

```
packitup -f json -m 10000000 -c -e *.log --no-content
```

## 📂 Output

PackItUp generates its output in a new directory named `<project_name>_structure_<timestamp>`. The main output file will be in this directory, named `<project_name>_structure_<timestamp>.<format>`.

If the compress option is used, a zip file will be created in the same directory.

The generated content is automatically copied to your clipboard for easy sharing.

## 🧹 Cleaning Up

To remove all PackItUp generated data:

```
packitup -p
```

This will delete the `.packitup` directory in your home folder and any local output directories.

## 🔄 Updating

To update PackItUp to the latest version, use pip:

```
pip install --upgrade packitup
```

## 🐛 Troubleshooting

If you encounter any issues while using PackItUp, try the following:

1. Ensure you have the latest version installed.
2. Check that you have the necessary permissions to read the files and directories you're trying to document.
3. If you're having issues with specific file types, try using the `--no-content` option to exclude file contents.

If problems persist, please open an issue on our GitHub repository.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request on our [GitHub repository](https://github.com/yourusername/packitup).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yourusername/packitup/blob/main/LICENSE) file for details.

## 🙏 Acknowledgements

- Thanks to all the open-source libraries that made this project possible.
- Special thanks to the Python community for their continuous support and inspiration.

---

Happy documenting! 📚✨
