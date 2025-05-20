#!/usr/bin/env python3
"""
verify_dependencies.py

Scan all Python files in the project (excluding venv, __pycache__, .git) and check that each imported module is installed in the current environment.

Usage:
    python verify_dependencies.py

Exits with code 0 if all dependencies are installed.
Exits with code 1 and lists missing modules if any are not installed.
"""
import os
import sys
import ast
import importlib

# Directories to ignore during scan
IGNORE_DIRS = {"venv", "__pycache__", ".git"}


def find_py_files(root):
    """Yield all .py file paths under root, skipping ignored directories."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Modify dirnames in-place to skip ignored dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fname in filenames:
            if fname.endswith(".py"):
                yield os.path.join(dirpath, fname)


def get_imported_modules(file_path):
    """Parse a .py file and return top-level module names imported."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            source = f.read()
            node = ast.parse(source, file_path)
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: skipping {file_path} due to parse error: {e}", file=sys.stderr)
            return set()
    modules = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                modules.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom):
            # Skip relative imports (level > 0)
            if n.level == 0 and n.module:
                modules.add(n.module.split('.')[0])
    return modules


def verify_modules(modules):
    """Attempt to import each module; return a list of those that fail."""
    missing = []
    for mod in sorted(modules):
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)
    return missing


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    all_modules = set()

    # Collect imports in all Python files
    for pyfile in find_py_files(project_root):
        all_modules.update(get_imported_modules(pyfile))

    # Verify each
    missing = verify_modules(all_modules)

    if missing:
        print("Missing dependencies detected:\n")
        for m in missing:
            print(f"  - {m}")
        print("\nPlease install them, e.g.:\n    pip install " + " ".join(missing))
        sys.exit(1)
    else:
        print("All dependencies are installed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
