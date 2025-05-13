import os
import subprocess
import requests
import re
from pathlib import Path


def generate_requirements(project_path: str) -> None:
    """Generate requirements.txt using pipreqs if it doesn't exist."""
    req_file = Path(project_path) / "requirements.txt"
    if not req_file.exists():
        print(
            f"No requirements.txt found in {project_path}. Generating one with pipreqs..."
        )
        try:
            # Ignore virtual environment and problematic directories
            ignore_dirs = ".venv312"
            subprocess.run(["pipreqs", project_path, "--force", "--ignore", ignore_dirs], check=True)
            print("Generated requirements.txt")
        except subprocess.CalledProcessError:
            print(
                "Error running pipreqs. Ensure it's installed (`pip install pipreqs`) or manually create requirements.txt."
            )
            print("Continuing without generating requirements.txt...")
            if not req_file.exists():
                with open(req_file, 'w') as f:
                    f.write("# Placeholder requirements.txt - add dependencies manually\n")
                print("Created placeholder requirements.txt")
    else:
        print(f"Found existing requirements.txt in {project_path}")


def get_latest_version(package: str) -> str:
    """Query PyPI API to get the latest version of a package."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.RequestException:
        print(f"Warning: Could not fetch latest version for {package}")
        return None


def update_requirements(project_path: str) -> None:
    """Update dependencies in requirements.txt to their latest versions."""
    req_file = Path(project_path) / "requirements.txt"
    if not req_file.exists():
        print(
            f"No requirements.txt found in {project_path}. Run generate_requirements first."
        )
        exit(1)

    # Read current requirements
    with open(req_file, "r") as f:
        lines = f.readlines()

    updated_lines = []
    updated_packages = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            updated_lines.append(line)
            continue

        # Match package==version or package>=version
        match = re.match(r"([a-zA-Z0-9_-]+)([>=]=[\d\.]+.*)?", line)
        if not match:
            print(f"Skipping invalid line: {line}")
            updated_lines.append(line)
            continue

        package = match.group(1)
        latest_version = get_latest_version(package)
        if latest_version:
            updated_lines.append(f"{package}=={latest_version}")
            print(f"Updated {package} to version {latest_version}")
            updated_packages.append((package, latest_version))
        else:
            updated_lines.append(line)  # Keep original if version fetch fails

    # Write updated requirements.txt
    with open(req_file, "w") as f:
        f.write("\n".join(updated_lines) + "\n")
    print(f"Updated {req_file}")

    # Print summary of updates
    if updated_packages:
        print("\nSummary of updated packages:")
        for package, version in updated_packages:
            print(f"- {package}: Updated to version {version}")
    else:
        print("\nNo packages were updated.")


def install_requirements(project_path: str) -> None:
    """Install dependencies from requirements.txt."""
    req_file = Path(project_path) / "requirements.txt"
    if not req_file.exists():
        print(f"No requirements.txt found in {project_path}")
        exit(1)

    print("Installing updated dependencies...")
    try:
        subprocess.run(["pip", "install", "-r", str(req_file)], check=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Check requirements.txt for conflicts.")


def main():
    # Get project path (default to current directory)
    project_path = (
        input(
            "Enter the project folder path (press Enter for current directory): "
        ).strip()
        or "."
    )
    project_path = str(Path(project_path).resolve())

    if not Path(project_path).is_dir():
        print(f"Error: {project_path} is not a valid directory")
        exit(1)

    # Generate requirements.txt if needed
    generate_requirements(project_path)

    # Update dependencies
    update_requirements(project_path)

    # Ask if user wants to install updated dependencies
    install = input("Install updated dependencies now? (y/n): ").strip().lower() == "y"
    if install:
        install_requirements(project_path)


if __name__ == "__main__":
    main()
