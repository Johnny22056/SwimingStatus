"""Standalone script to open a native macOS folder selection dialog using osascript.
Prints the selected folder path to stdout, or empty string if cancelled.
"""
import subprocess
import sys


def main():
    initial_dir = sys.argv[1] if len(sys.argv) > 1 else "~"
    
    # Use AppleScript to show native folder dialog
    script = f'''
    set defaultFolder to POSIX file "{initial_dir}" as alias
    try
        set selectedFolder to choose folder with prompt "Select Screenshot Folder" default location defaultFolder
        return POSIX path of selectedFolder
    on error
        return ""
    end try
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=120
        )
        folder = result.stdout.strip()
        print(folder)
    except Exception:
        print("")


if __name__ == "__main__":
    main()
