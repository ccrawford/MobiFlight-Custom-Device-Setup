import os
import shutil
import sys
import fileinput
from pathlib import Path

def replace_in_file(file_path, replacements):
    """Replace all keys in `replacements` with their values in the given file."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def rename_files_and_directories(base_path, replacements):
    """Recursively rename files and directories based on replacements."""
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Rename files
        for name in files:
            old_path = Path(root) / name
            new_name = name
            for old, new in replacements.items():
                new_name = new_name.replace(old, new)
            new_path = Path(root) / new_name
            old_path.rename(new_path)

        # Rename directories
        for name in dirs:
            old_path = Path(root) / name
            new_name = name
            for old, new in replacements.items():
                new_name = new_name.replace(old, new)
            new_path = Path(root) / new_name
            old_path.rename(new_path)


def main(template_path, device_name, prefix):
    # Ensure template_path exists
    template_path = Path(template_path)
    if not template_path.is_dir():
        print(f"Template path {template_path} does not exist.")
        sys.exit(1)

    # Locate the 'Template' folder
    template_folder = template_path / "Template"
    if not template_folder.is_dir():
        print(f"No 'Template' folder found inside {template_path}.")
        sys.exit(1)

    # Rename the Template folder to DEVICE_NAME
    new_device_path = template_path / device_name
    if new_device_path.exists():
        print(f"Device folder '{new_device_path}' already exists.")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != "y":
            print("Operation canceled.")
            sys.exit(1)
        shutil.rmtree(new_device_path)  # Remove the existing directory

    # Perform the rename
    template_folder.rename(new_device_path)

    # Continue with renaming files and updating contents within the renamed folder
    rename_files_and_directories(new_device_path, {
        "MyCustomClass.cpp": f"{device_name}.cpp",
        "MyCustomClass.h": f"{device_name}.h",
        "MyCustomDevice_platformio.ini": f"{device_name}_platformio.ini",
    })

    replacements = {
        "MyCustomClass": device_name,
        "Mobiflight Template": f"{prefix} {device_name}",
        "mobiflight_template": f"{prefix.lower()}_{device_name.lower()}",
        "Template": device_name,
        "YourProject": device_name,
        "MOBIFLIGHT_TEMPLATE": device_name,
        "env_template": f"env_{device_name}",
    }

    # Update content in relevant files
    for file_path in new_device_path.rglob("*.cpp"):
        replace_in_file(file_path, replacements)

    for file_path in new_device_path.rglob("*.h"):
        replace_in_file(file_path, replacements)

    for file_path in new_device_path.rglob("*_platformio.ini"):
        replace_in_file(file_path, replacements)

    # Update Community boards and devices
    community_path = new_device_path / "Community"
    for file_path in community_path.glob("boards/*.json"):
        replace_in_file(file_path, {
            "mobiflight_template": f"{prefix.lower()}_{device_name.lower()}",
            "Mobiflight Template": f"{prefix} {device_name}",
            "MOBIFLIGHT_TEMPLATE": device_name,
        })

    for file_path in community_path.glob("devices/*.json"):
        replace_in_file(file_path, {
            "MOBIFLIGHT_TEMPLATE": device_name,
            "Mobiflight": prefix,
            "template": device_name,
        })

    # Rename JSON files in boards and devices
    rename_files_and_directories(community_path / "boards", {
        "mobiflight_template": device_name,
    })
    rename_files_and_directories(community_path / "devices", {
        "mobiflight.template": f"{prefix.lower()}.{device_name.lower()}",
    })

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python setup_project.py <template_path> <DEVICE_NAME> <PREFIX>")
        sys.exit(1)

    template_path_arg = sys.argv[1]
    device_name_arg = sys.argv[2]
    prefix_arg = sys.argv[3]

    main(template_path_arg, device_name_arg, prefix_arg)
