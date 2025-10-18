"""Build script for creating standalone executable with Nuitka."""

import subprocess
import sys
import platform
import shutil
from pathlib import Path


def get_platform_name():
    """Get current platform name."""
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        return "unknown"


def check_nuitka():
    """Check if Nuitka is installed."""
    try:
        subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def build_windows():
    """Build for Windows."""
    print("🪟 Building for Windows...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",                      # Standalone executable
        "--onefile",                         # Single file
        "--enable-plugin=pyside6",           # PySide6 support
        "--windows-disable-console",         # No console window
        "--windows-icon-from-ico=resources/icons/notehub.ico" if Path("resources/icons/notehub.ico").exists() else "",
        "--company-name=NoteHub",
        "--product-name=NoteHub Desktop",
        "--file-version=1.0.0",
        "--product-version=1.0.0",
        "--file-description=NoteHub Desktop Application",
        "--output-dir=dist",
        "--output-filename=NoteHub.exe",
        "src/main.py"
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    subprocess.run(cmd, check=True)
    print("✅ Build complete: dist/NoteHub.exe")


def build_linux():
    """Build for Linux."""
    print("🐧 Building for Linux...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyside6",
        "--linux-icon=resources/icons/notehub.png" if Path("resources/icons/notehub.png").exists() else "",
        "--output-dir=dist",
        "--output-filename=NoteHub",
        "src/main.py"
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    subprocess.run(cmd, check=True)
    print("✅ Build complete: dist/NoteHub")


def build_macos():
    """Build for macOS."""
    print("🍎 Building for macOS...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=pyside6",
        "--macos-create-app-bundle",
        "--macos-app-icon=resources/icons/notehub.icns" if Path("resources/icons/notehub.icns").exists() else "",
        "--macos-app-name=NoteHub",
        "--output-dir=dist",
        "src/main.py"
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    subprocess.run(cmd, check=True)
    print("✅ Build complete: dist/NoteHub.app")


def clean():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "src/__pycache__", "src/**/__pycache__"]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed: {path}")


def main():
    """Main build function."""
    # Check Nuitka
    if not check_nuitka():
        print("❌ Nuitka is not installed!")
        print("Install with: pip install nuitka")
        sys.exit(1)
    
    # Get platform
    if len(sys.argv) > 1:
        target_platform = sys.argv[1].lower()
    else:
        target_platform = get_platform_name()
    
    # Special commands
    if target_platform == "clean":
        clean()
        return
    
    print(f"🚀 NoteHub Desktop Build Script")
    print(f"📦 Target platform: {target_platform}")
    print()
    
    # Build
    try:
        if target_platform == "windows":
            build_windows()
        elif target_platform == "linux":
            build_linux()
        elif target_platform == "macos":
            build_macos()
        else:
            print(f"❌ Unknown platform: {target_platform}")
            print("Usage: python build.py [windows|linux|macos|clean]")
            sys.exit(1)
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Build cancelled")
        sys.exit(130)


if __name__ == "__main__":
    main()
