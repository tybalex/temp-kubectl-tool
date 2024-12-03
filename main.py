import asyncio
import json
import os
import sys
import subprocess
import gptscript
import shlex


# from: https://github.com/otto8-ai/tools/blob/main/google/gmail/helpers.py#L277C1-L312C46
def prepend_base_path(base_path: str, file_path: str):
    """
    Prepend a base path to a file path if it's not already rooted in the base path.

    Args:
        base_path (str): The base path to prepend.
        file_path (str): The file path to check and modify.

    Returns:
        str: The modified file path with the base path prepended if necessary.

    Examples:
      >>> prepend_base_path("files", "my-file.txt")
      'files/my-file.txt'

      >>> prepend_base_path("files", "files/my-file.txt")
      'files/my-file.txt'

      >>> prepend_base_path("files", "foo/my-file.txt")
      'files/foo/my-file.txt'

      >>> prepend_base_path("files", "bar/files/my-file.txt")
      'files/bar/files/my-file.txt'

      >>> prepend_base_path("files", "files/bar/files/my-file.txt")
      'files/bar/files/my-file.txt'
    """
    # Split the file path into parts for checking
    file_parts = os.path.normpath(file_path).split(os.sep)

    # Check if the base path is already at the root
    if file_parts[0] == base_path:
        return file_path

    # Prepend the base path
    return os.path.join(base_path, file_path)


async def save_to_gptscript_workspace(filepath: str, content: str) -> None:
    gptscript_client = gptscript.GPTScript()
    wksp_file_path = prepend_base_path('files', filepath)
    await gptscript_client.write_file_to_workspace(wksp_file_path, content.encode('utf-8'))


async def main():
    # Set up argument parser
    if len(sys.argv) < 2:
        print("Usage: python main.py <kubectl-arguments>")
        sys.exit(1)
    base_command = sys.argv[1:]
    # Get parameters from either environment variables or command line arguments
    command = os.getenv("COMMAND")
    output_file = os.getenv("OUTPUT_FILE")
    # kubectl_command = ["kubectl", "get", "pods", "-n", "default"]
    if not command:
        print("COMMAND is not set, it is required.")
        sys.exit(1)
    if command:
        command_args = shlex.split(command)
        kubectl_command = base_command + command_args
    else:
        kubectl_command = base_command

    try:
        # Run the command
        result = subprocess.run(kubectl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # Output the result
        if output_file:
            try:
                await save_to_gptscript_workspace(output_file, result.stdout)
                print(f"Output has been saved to {output_file} in the workspace files directory.")
            except Exception as e:
                print("Failed to save to workspace, saving to local file instead.")
                with open(output_file, "w") as f:
                    f.write(result.stdout)
        else:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred when executing the command:")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())