def archive_and_purge(output_dir):
    """Compress the output directory and then purge it."""
    archive_file = f"{output_dir}.zip"
    with zipfile.ZipFile(archive_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), output_dir),
                )
    shutil.rmtree(output_dir)
    return archive_file


def prompt_user_for_confirmation(message):
    """Prompt user for confirmation."""
    response = input(f"{Fore.YELLOW}{message} (y/n): {Fore.RESET}").strip().lower()
    return response in ["y", "yes"]


def purge_data():
    home_dir = os.path.expanduser("~")
    home_packitup_dir = os.path.join(home_dir, ".packitup")
    purge_options = [
        (home_packitup_dir, "PackItUp data"),
        (os.path.join(os.getcwd(), "packitup_structure"), "local output directories"),
    ]

    print(f"{Fore.CYAN}Purging Options:{Fore.RESET}")
    for path, description in purge_options:
        print(f"  - {description}: {path}")

    if not prompt_user_for_confirmation(
        "Are you sure you want to purge the above data?"
    ):
        print(f"{Fore.YELLOW}⚠️ Purge operation cancelled.{Fore.RESET}")
        return

    # Archive and purge PackItUp data
    for path, description in purge_options:
        if os.path.exists(path):
            try:
                archive_file = archive_and_purge(path)
                print(
                    f"{Fore.GREEN}✅ Successfully archived and purged {description} from {path}"
                )
                print(f"{Fore.YELLOW}📦 Archive created at {archive_file}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error while purging {description}: {e}")
        else:
            print(f"{Fore.YELLOW}⚠️ No {description} found to purge.")

    print(f"{Fore.GREEN}✅ Purge operation completed.{Fore.RESET}")


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

    if args.tree:
        skip_patterns += TREE_ONLY_SKIP_FOLDERS

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    root_folder_name = os.path.basename(root_dir)

    with tempfile.TemporaryDirectory() as tmp_output_dir:
        output_dir = os.path.join(
            tmp_output_dir, f"{root_folder_name}_structure_{timestamp}"
        )
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

        if not args.tree:
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
                f"📋 Content has been copied to clipboard." if not args.tree else "",
                f"📂 Large files have been split and saved in parts if necessary.",
                f"🗂️  Skipped patterns: {', '.join(skip_patterns + gitignore_patterns)}",
            ],
        )


if __name__ == "__main__":
    main()
