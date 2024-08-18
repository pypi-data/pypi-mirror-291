import os
import shutil

def prompt_for_directory(prompt_message, default_directory=None):
    """Prompt the user for a directory and return it if valid."""
    while True:
        directory = input(f"{prompt_message} [{default_directory}]: ").strip()
        if not directory and default_directory:
            directory = default_directory
        if os.path.isdir(directory):
            return directory
        else:
            print(f"Directory '{directory}' does not exist. Please try again.")

def prompt_for_file(prompt_message):
    """Prompt the user for a file path and return it if valid."""
    while True:
        file_path = input(f"{prompt_message}: ").strip()
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"File '{file_path}' does not exist. Please try again.")

def append_to_php_ini(php_ini_path, extensions):
    """Append lines to php.ini if they are not already present, ensuring proper newlines."""
    try:
        with open(php_ini_path, 'a+') as php_ini_file:
            php_ini_file.seek(0)  # Move to the beginning of the file to read existing lines
            existing_lines = php_ini_file.readlines()
            
            # Check if the file ends with a newline
            if existing_lines and not existing_lines[-1].endswith('\n'):
                php_ini_file.write('\n')  # Add a newline if the last line doesn't end with one
            
            # Append only the lines that are not already present
            for extension in extensions:
                if not any(line.strip() == extension for line in existing_lines):
                    php_ini_file.write(f"{extension}\n")
                    # print(f"Added '{extension}' to {php_ini_path}")
    except PermissionError:
        print(f"Permission denied: Unable to write to {php_ini_path}. Please check your file permissions.")
    except Exception as e:
        print(f"An error occurred while updating {php_ini_path}: {e}")

def main():
    default_source_dir = '/usr/local/extensions'
    source_dir = prompt_for_directory(
        "Please enter the path to the source directory",
        default_directory=default_source_dir
    )

    php_ext_dir = prompt_for_directory(
        "Please enter the path to the PHP extension directory"
    )

    php_ini_path = prompt_for_file(
        "Please enter the path to the php.ini file"
    )

    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

    if not os.path.isdir(php_ext_dir):
        raise FileNotFoundError(f"PHP extension directory '{php_ext_dir}' does not exist.")

    so_files = [f for f in os.listdir(source_dir) if f.endswith('.so')]

    for so_file in so_files:
        src_path = os.path.join(source_dir, so_file)
        dest_path = os.path.join(php_ext_dir, so_file)
        
        try:
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                # print(f"Copied {so_file} to {php_ext_dir}")
            else:
                print(f"Source file {src_path} does not exist.")
        except PermissionError:
            print(f"Permission denied: Unable to copy {so_file}. Please check your file permissions.")
        except Exception as e:
            print(f"An error occurred while copying {so_file}: {e}")

    extensions_to_add = [
        "extension=secureai.so",
        "extension=encai.so",
        "extension=secencryptai.so"
    ]
    
    if os.path.isfile(php_ini_path):
        append_to_php_ini(php_ini_path, extensions_to_add)
    else:
        print(f"php.ini file '{php_ini_path}' does not exist.")

    print("Extraction completed.")

if __name__ == "__main__":
    main()