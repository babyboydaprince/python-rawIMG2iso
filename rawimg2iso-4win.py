import lzma
import os
import subprocess
import sys
import shutil

def decompress_raw_xz(input_file, output_file):
    """Decompress a .xz file to .raw format."""
    try:
        with lzma.open(input_file, 'rb') as xz_file, open(output_file, 'wb') as raw_file:
            raw_file.write(xz_file.read())
        print(f"Decompressed {input_file} to {output_file}")
    except Exception as e:
        print(f"Error decompressing {input_file}: {e}")
        sys.exit(1)

def convert_raw_to_iso(input_file, output_iso):
    """Convert a .raw file to .iso format using mkisofs or genisoimage on Windows."""
    try:
        # Ensure mkisofs.exe is in the PATH or specify the full path to the executable
        mkisofs_path = shutil.which("mkisofs") or shutil.which("genisoimage")
        if not mkisofs_path:
            raise FileNotFoundError("mkisofs or genisoimage is not found in PATH. Please install it.")

        command = [
            mkisofs_path,
            "-o", output_iso,
            "-input-charset", "utf-8",
            input_file
        ]
        subprocess.run(command, check=True)
        print(f"Converted {input_file} to {output_iso}")
    except FileNotFoundError:
        print("Error: mkisofs or genisoimage is not installed. Please install it and try again.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file} to {output_iso}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python rawimg2iso-4win.py <input_file.raw.xz> <output_file.iso>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_iso = sys.argv[2]

    if not input_file.endswith(".raw.xz"):
        print("Error: Input file must have a .raw.xz extension.")
        sys.exit(1)

    temp_raw_file = input_file.replace(".xz", "")

    # Step 1: Decompress the .raw.xz file
    decompress_raw_xz(input_file, temp_raw_file)

    # Step 2: Convert the .raw file to .iso format
    convert_raw_to_iso(temp_raw_file, output_iso)

    # Step 3: Clean up the temporary .raw file
    try:
        os.remove(temp_raw_file)
        print(f"Cleaned up temporary file: {temp_raw_file}")
    except OSError as e:
        print(f"Error removing temporary file: {e}")

if __name__ == "__main__":
    main()
