# PDF Password Batch Tool

This is a command-line tool written in Python designed to help you process multiple PDF files that share the same password. You can either batch remove the password from all files or batch change them to a new, unified password.

## ✨ Features

- **Batch Remove Passwords**: Quickly unlock all PDFs in a directory and save them as password-free versions.
- **Batch Change Passwords**: Update the old password on all PDFs to a new one you specify.
- **Secure Password Entry**: If you prefer not to type your password directly into the command line, you can omit the password argument, and the script will prompt you to enter it securely without showing it on screen.
- **Progress Bar**: Uses `tqdm` to display a progress bar, so you know which file is being processed.
- **Cross-Platform**: Built with Python, it runs on Windows, macOS, and Linux.
- **Local & Secure**: All operations are performed on your local machine, ensuring the privacy and security of your documents.

## ⚙️ Prerequisites

You will need Python 3.7 or a newer version installed on your system.

## 🚀 Installation & Setup

1.  **Clone the Repository**
    Download or clone this project from GitHub.
    ```bash
    git clone [https://github.com/YOUR_USERNAME/pdf_password_tool.git](https://github.com/YOUR_USERNAME/pdf_password_tool.git)
    cd pdf_password_tool
    ```

2.  **Create a Virtual Environment (Recommended)**
    It's best practice to use a virtual environment to manage project dependencies.
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Use `pip` to install all the required libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## 📝 Usage

This tool provides two main commands: `remove` and `change`.

**Basic Command Structure:**
```
python main.py [command] --input-dir "path/to/input/folder" --output-dir "path/to/output/folder" [options]
```

---

### Example 1: Remove Passwords from all PDFs

Let's say your PDFs are located in `C:\MyPDFFiles`, their current password is `old_password`, and you want to save the unlocked files to `C:\UnlockedPDFFiles`.

```bash
python main.py remove --input-dir "C:\MyPDFFiles" --output-dir "C:\UnlockedPDFFiles" --password "old_password"
```

**Secure Mode (Recommended):**
If you don't want to expose the password in your command history, omit the `--password` flag, and the script will prompt you to enter it:
```bash
python main.py remove --input-dir "C:\MyPDFFiles" --output-dir "C:\UnlockedPDFFiles"
```
The terminal will then display:
```
Enter the current PDF password:
```
(Your password input will be hidden)

---

### Example 2: Change the Password for all PDFs

Let's say you want to change the password for all PDFs in `C:\MyPDFFiles` from `old_password` to `new_secure_password` and save them to `C:\NewPasswordPDFFiles`.

```bash
python main.py change --input-dir "C:\MyPDFFiles" --output-dir "C:\NewPasswordPDFFiles" --current-password "old_password" --new-password "new_secure_password"
```

**Secure Mode (Recommended):**
Similarly, you can omit the password arguments to be prompted securely:
```bash
python main.py change --input-dir "C:\MyPDFFiles" --output-dir "C:\NewPasswordPDFFiles"
```
The terminal will then prompt you for both passwords:
```
Enter the current PDF password:
Enter the new PDF password:
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).