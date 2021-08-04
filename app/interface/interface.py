import os
import sys
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter import filedialog
import pathlib

from app.functions.read_checksum_file import ChecksumFile


class ChecksumChecker(object):
    def __init__(self):
        self.form()

    def form(self):
        # Create and configure the main window
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.configure(bg="white")
        self.window.iconbitmap(self.resource_path("app/static/favicon.ico"))
        self.window.title("Checksum Checker")

        # Add a frame to hold all other components
        frame = tk.Frame()
        frame.configure(bg="white", borderwidth=0)

        # A canvas with the WRGL logo as a header
        canvas = tk.Canvas(frame, width=800, height=100)
        canvas.configure(bg="white", borderwidth=0)
        canvas.pack()
        img = tk.PhotoImage(file=self.resource_path("app/static/WRGL_logo.png"))
        canvas.create_image(400, 50, anchor=tk.CENTER, image=img)

        # Button to load a file picker
        self.chosenfiles = []
        load_picker = tk.Button(
            frame, text="Select files", command=self.open_filepicker,
        )
        load_picker.pack()

        # TODO
        # Display a list of the chosen files

        # Run the checking (TODO)
        run = tk.Button(frame, text="Check", command=self.run_checker)
        run.pack()

        # scrolling text window (as we'll almost certainly be checking many files at
        # once)
        self.text_window = tkscrolled.ScrolledText(frame, heigh=20, wrap='word')
        self.text_window.configure(bg="black", fg="white")
        self.text_window.insert(
            tk.END,
            """certUtil Checksum Checker
-------------------------

Version: 1.0 (2020-06-19)
Support: ben.sanders@nhs.net
-------------------------

Select .md5 checksum files to confirm using the "Select Files" button, then
click the "Check" button to start. This may take some time, particularly if the
files to be checked are very large.

When complete, a summary list of any failing files will be shown.

Do not complete the backup process if there are any failing files. Repeat the
transfer and check again.
""",
        )
        self.text_window.pack()

        # Pack the frame (and contents) into the window
        frame.pack()

        self.window.update()
        self.window.mainloop()

    def open_filepicker(self):
        fnames = filedialog.askopenfilenames(
            initialdir="/",
            title="Select file",
            filetypes=(("checksum files", "*.md5"), ("all files", "*.*")),
            multiple=True,
        )
        fnames = list(fnames)

        if fnames:
            self.chosenfiles = []
            self.text_window.delete(1.0, tk.END)
            for fname in fnames:
                fname = pathlib.Path(fname)
                if fname.suffix == ".md5":
                    self.text_window.insert(tk.END, f"{fname.name}\n")
                    self.chosenfiles.append(fname)
            self.window.update()

    def run_checker(self):
        # Record any failing files
        errorlist = []

        if self.chosenfiles:
            # Track the number of files to check so we can give a progress indicator
            total = len(self.chosenfiles)
            current = 1

            # Clear existing text
            self.text_window.delete(1.0, tk.END)
            for fname in self.chosenfiles:
                # Use pathlib to extract just the name from the file path
                name = fname.name

                # Print the name of the file being checked, and force and update of the
                # text box
                self.text_window.insert(tk.END, f"{current}/{total}: {name}...")
                self.window.update()

                # Do the check, and update the text box as appropriate
                checker = ChecksumFile(fname)
                if checker.hash_ok:
                    self.text_window.insert(tk.END, "\tOK\n")
                    del checker
                else:
                    self.text_window.insert(tk.END, "\tERROR\n")
                    errorlist.append(checker)
                self.window.update()

                # Update progress counter
                current += 1

            if not errorlist:
                self.text_window.insert(tk.END, "\n----------------------------\n")
                self.text_window.insert(tk.END, "All file hashes match.")
            else:
                self.text_window.insert(tk.END, "\n----------------------------\n")
                self.text_window.insert(tk.END, "Mismatched hashes detected for the following files:\n\n")
                # Report the name of each failed checksum
                for failed in errorlist:
                    self.text_window.insert(tk.END, f"{failed.checksum_file_name}")

        else:
            pass

    @staticmethod
    def resource_path(relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    form = ChecksumChecker()
