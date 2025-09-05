# main.py
import argparse
import getpass
import os
from pathlib import Path
from tqdm import tqdm
import pypdf

# --- Core Processing Function ---
def process_pdfs(input_dir: Path, output_dir: Path, current_password: str, new_password: str = None):
    """
    Batch process PDF files to remove or change their passwords.
    This function recursively searches for PDFs in all subdirectories.

    :param input_dir: Path to the root directory containing the input PDFs.
    :param output_dir: Path to the root directory where the processed PDFs will be saved.
    :param current_password: The current password for all PDF files.
    :param new_password: The new password to set. If None, the password will be removed.
    """
    if not input_dir.is_dir():
        print(f"Error: Input path '{input_dir}' is not a valid directory.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory '{output_dir}' has been verified or created.")

    # Use **/*.pdf to recursively find all PDF files in all subdirectories.
    pdf_files = list(input_dir.glob('**/*.pdf'))

    if not pdf_files:
        print(f"No PDF files found in '{input_dir}' or any of its subdirectories.")
        return

    print(f"Found {len(pdf_files)} PDF files. Starting process...")

    # Use tqdm for a progress bar
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            # Determine the output path while preserving the subdirectory structure
            relative_path = pdf_path.relative_to(input_dir)
            output_path = output_dir / relative_path
            
            # Create the necessary subdirectories in the output folder
            output_path.parent.mkdir(parents=True, exist_ok=True)

            reader = pypdf.PdfReader(pdf_path)

            if not reader.is_encrypted:
                tqdm.write(f"Note: '{relative_path}' is not encrypted. Copying file directly.")
                # If not encrypted, just copy the file
                writer = pypdf.PdfWriter()
                writer.clone_reader_document(reader)
            else:
                # Attempt to decrypt with the current password
                if reader.decrypt(current_password) == pypdf.PasswordType.NOT_DECRYPTED:
                    tqdm.write(f"Error: Incorrect password for '{relative_path}'. Skipping file.")
                    continue
                
                writer = pypdf.PdfWriter()
                # Copy all pages
                for page in reader.pages:
                    writer.add_page(page)

            # If a new password is provided, encrypt the file with it
            if new_password:
                writer.encrypt(new_password)

            # Save the processed file to the output directory
            with open(output_path, 'wb') as f:
                writer.write(f)

        except Exception as e:
            tqdm.write(f"An unknown error occurred while processing '{pdf_path.name}': {e}. Skipping file.")

    print("\nAll files have been processed successfully!")


# --- Main Program Entry Point ---
def main():
    parser = argparse.ArgumentParser(
        description="A command-line tool to batch process PDF passwords, with subdirectory support.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # --- Remove Password Command ---
    parser_remove = subparsers.add_parser('remove', help='Remove passwords from PDF files in a directory and its subdirectories.')
    parser_remove.add_argument('-i', '--input-dir', type=str, required=True, help='Root directory containing the PDFs to process.')
    parser_remove.add_argument('-o', '--output-dir', type=str, required=True, help='Root directory to save the unlocked PDFs.')
    parser_remove.add_argument('-p', '--password', type=str, help='The current password for the PDFs.\nIf omitted, you will be prompted to enter it securely.')

    # --- Change Password Command ---
    parser_change = subparsers.add_parser('change', help='Change the password for PDF files in a directory and its subdirectories.')
    parser_change.add_argument('-i', '--input-dir', type=str, required=True, help='Root directory containing the PDFs to process.')
    parser_change.add_argument('-o', '--output-dir', type=str, required=True, help='Root directory to save the re-encrypted PDFs.')
    parser_change.add_argument('-p', '--current-password', type=str, help='The current password for the PDFs.\nIf omitted, you will be prompted to enter it securely.')
    parser_change.add_argument('-n', '--new-password', type=str, help='The new password to set for the PDFs.\nIf omitted, you will be prompted to enter it securely.')

    args = parser.parse_args()

    # Convert path strings to Path objects
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    # Execute the appropriate action based on the command
    if args.command == 'remove':
        current_pass = args.password if args.password else getpass.getpass("Enter the current PDF password: ")
        process_pdfs(input_dir, output_dir, current_pass, new_password=None)

    elif args.command == 'change':
        current_pass = args.current_password if args.current_password else getpass.getpass("Enter the current PDF password: ")
        new_pass = args.new_password if args.new_password else getpass.getpass("Enter the new PDF password: ")
        process_pdfs(input_dir, output_dir, current_pass, new_password=new_pass)


if __name__ == '__main__':
    main()