#!/usr/bin/env python3
"""
check_and_install_deps.py

Check and install missing dependencies for a given Python file.

Usage:
    python check_and_install_deps.py path/to/your_script.py
"""

import sys
import ast
import importlib
import subprocess
import os

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

def install_modules(modules):
    """Install missing modules using pip."""
    if not modules:
        return
    print(f"Installing missing modules: {' '.join(modules)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *modules])

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_and_install_deps.py path/to/your_script.py")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    modules = get_imported_modules(file_path)
    missing = verify_modules(modules)
    if missing:
        print("Missing dependencies detected:")
        for m in missing:
            print(f"  - {m}")
        install_modules(missing)
    else:
        print("All dependencies are installed.")

if __name__ == '__main__':
    main()
