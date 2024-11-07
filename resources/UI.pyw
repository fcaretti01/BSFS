import os
import tkinter as tk
from tkinter import ttk, messagebox

class PDFExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Explorer")
        self.root.geometry("500x450")
        
        # Set up directories for each type of resource
        self.directoriesdict = {
            "Books": ["./resources/books", "./books"],
            "Articles": ["./resources/articles", "./articles"],
            "Papers": ["./resources/papers", "./papers"]
        }
        
        # Selected resource type and PDF paths
        self.selected_type = tk.StringVar(value="Books")
        self.pdf_paths = []

        # Dropdown menu for resource type selection
        resource_label = tk.Label(self.root, text="Select Resource Type:")
        resource_label.pack(pady=5)
        
        resource_menu = ttk.Combobox(self.root, textvariable=self.selected_type, values=list(self.directoriesdict.keys()), state="readonly")
        resource_menu.pack(fill=tk.X, padx=10)
        resource_menu.bind("<<ComboboxSelected>>", self.update_pdf_list)

        # Search bar
        self.search_var = tk.StringVar()
        search_label = tk.Label(self.root, text="Search:")
        search_label.pack(pady=5)
        
        search_entry = tk.Entry(self.root, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, padx=10)
        search_entry.bind("<KeyRelease>", self.update_pdf_list)
        
        # PDF list display
        self.pdf_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.pdf_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Open button
        open_button = tk.Button(self.root, text="Open PDF", command=self.open_pdf)
        open_button.pack(pady=5)

        # Initial list update
        self.update_pdf_list()

    def get_pdf_paths(self, directories):
        """Retrieve PDF files in a specific directory."""
        pdf_paths = []
        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".pdf"):
                        pdf_paths.append(os.path.join(root, file))
        return pdf_paths

    def update_pdf_list(self, event=None):
        """Update the displayed list of PDFs based on the selected type and search query."""
        # Clear current listbox content
        self.pdf_listbox.delete(0, tk.END)

        # Get selected resource type and directory
        selected_type = self.selected_type.get()
        directories = self.directoriesdict.get(selected_type, "")

        # Retrieve PDFs from selected directory and filter by search query
        self.pdf_paths = self.get_pdf_paths(directories)
        query = self.search_var.get().lower()
        
        for pdf_path in self.pdf_paths:
            pdf_name = os.path.basename(pdf_path)
            if query in pdf_name.lower():
                self.pdf_listbox.insert(tk.END, pdf_name)

    def open_pdf(self):
        """Open the selected PDF file."""
        selected_index = self.pdf_listbox.curselection()
        if selected_index:
            pdf_name = self.pdf_listbox.get(selected_index)
            pdf_path = next((p for p in self.pdf_paths if os.path.basename(p) == pdf_name), None)
            
            if pdf_path:
                os.startfile(pdf_path)
            else:
                messagebox.showerror("Error", "Could not find the PDF file.")
        else:
            messagebox.showwarning("Warning", "Please select a PDF from the list.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFExplorerApp(root)
    root.mainloop()
