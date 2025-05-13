import os
import ast
import sys

def check_syntax(file_path):
    """Check if a Python file has syntax errors using ast.parse()."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f'SyntaxError: {str(e)}'
    except Exception as e:
        return False, f'Other error: {str(e)}'

def scan_directory(directory):
    """Scan a directory recursively for Python files and check for syntax errors."""
    error_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                success, error_msg = check_syntax(file_path)
                if not success:
                    error_files.append((file_path, error_msg))
                    print(f'Error in {file_path}: {error_msg}')
    return error_files

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f'Scanning directory: {directory}')
    errors = scan_directory(directory)
    if errors:
        print(f'Found {len(errors)} files with syntax errors.')
        for file_path, error_msg in errors:
            print(f'- {file_path}: {error_msg}')
    else:
        print('No syntax errors found in Python files.')
