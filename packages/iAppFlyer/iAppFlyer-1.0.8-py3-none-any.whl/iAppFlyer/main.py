import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
import threading
import requests
from io import BytesIO

class AppCenterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iAppFlyer")

        # Adjust the window size (width x height)
        self.window_width = 600
        self.window_height = 630  # Reduced height

        # Set window size
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Center the window on the screen
        self.center_window()

        self.root.configure(bg="#f0f0f0")

        # Initialize state variables
        self.upload_in_progress = False
        self.dot_index = 0

        # Create frames for different sections
        self.frame_main = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        self.create_main_screen()

        # Ensure all widgets are visible and updated
        self.root.update_idletasks()

    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()  # Update "requested size" from geometry manager
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def create_main_screen(self):
        """Create the file upload screen."""
        # Download and load the image from the URL
        logo_url = "https://storage.googleapis.com/static-cms-prod/2023/10/color.png"
        response = requests.get(logo_url)
        logo_image = Image.open(BytesIO(response.content))
        logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        # Create a frame for the logo and title
        frame_title = tk.Frame(self.frame_main, bg="#f0f0f0", padx=20, pady=10)
        frame_title.pack(fill=tk.X, pady=20)

        # Add the logo and title to the frame
        logo_label = tk.Label(frame_title, image=self.logo_photo, bg="#f0f0f0")
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add a label to center-align the title text
        center_frame = tk.Frame(frame_title, bg="#f0f0f0")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(center_frame, text="iAppFlyer", font=("Helvetica", 24, "bold"), fg="#000000", bg="#f0f0f0")
        title_label.pack(pady=10)

        # File Path
        tk.Label(self.frame_main, text="File Path:", bg="#f0f0f0", font=("Arial", 16)).pack(anchor=tk.W, padx=20, pady=(20, 5))
        self.entry_file_path = tk.Entry(self.frame_main, width=50, font=("Arial", 14))
        self.entry_file_path.pack(padx=20, pady=(0, 10))
        tk.Button(self.frame_main, text="Browse", command=self.browse_file, bg="#007bff", fg="black", font=("Arial", 14, "bold"), relief=tk.RAISED).pack(pady=10)

        # Build Version
        tk.Label(self.frame_main, text="Build Version:", bg="#f0f0f0", font=("Arial", 16)).pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.entry_build_version = tk.Entry(self.frame_main, font=("Arial", 14))
        self.entry_build_version.pack(padx=20, pady=(0, 10))

        # Group
        tk.Label(self.frame_main, text="Group:", bg="#f0f0f0", font=("Arial", 16)).pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.group_var = tk.StringVar(value="QA")
        self.dropdown_group = tk.OptionMenu(self.frame_main, self.group_var, "QA", "Collaborators")
        self.dropdown_group.config(font=("Arial", 14), bg="#ffffff", fg="#007bff")
        self.dropdown_group.pack(padx=20, pady=(0, 20))

        # Distribute Release Button
        self.distribute_button = tk.Button(self.frame_main, text="Distribute Release", command=self.start_upload, bg="#28a745", fg="black", font=("Arial", 18, "bold"), relief=tk.RAISED)
        self.distribute_button.pack(pady=20, ipadx=10, ipady=10)  # Increase button size

        # Loader and progress message
        self.progress_frame = tk.Frame(self.frame_main, bg="#f0f0f0")
        self.progress_frame.pack(pady=20)

        self.uploading_label = tk.Label(self.progress_frame, text="Uploading", font=("Helvetica", 18, "italic"), bg="#f0f0f0", fg="#0000ff")  # Updated color to blue
        self.uploading_label.pack(side=tk.LEFT, padx=5)

        self.dot_label = tk.Label(self.progress_frame, text="", font=("Helvetica", 24), bg="#f0f0f0")
        self.dot_label.pack(side=tk.LEFT)

        self.progress_message = tk.Label(self.frame_main, text="", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.progress_message.pack(pady=20)

        # Hide progress elements initially
        self.uploading_label.pack_forget()
        self.dot_label.pack_forget()
        self.progress_message.pack_forget()

    def browse_file(self):
        """Open file dialog to select a file."""
        filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        self.entry_file_path.delete(0, tk.END)
        self.entry_file_path.insert(0, filename)

    def start_upload(self):
        """Start the upload process."""
        if self.upload_in_progress:
            return

        file_path = self.entry_file_path.get()
        build_version = self.entry_build_version.get()

        if not file_path or not build_version:
            self.show_popup("All fields are required.", "Error")
            return

        self.upload_in_progress = True
        self.distribute_button.config(state=tk.DISABLED)  # Disable the button
        self.uploading_label.pack(side=tk.LEFT, padx=5)  # Show "Uploading" text
        self.dot_label.pack(side=tk.LEFT)  # Show dot animation
        self.progress_message.pack(pady=20)  # Show progress message

        self.reset_progress_screen()
        threading.Thread(target=self.distribute_release, daemon=True).start()

    def reset_progress_screen(self):
        """Reset the progress screen elements."""
        self.dot_index = 0  # Reset the dot animation
        self.progress_message.config(text="", fg="#000000")
        self.uploading_label.config(text="Uploading")  # Set text to "Uploading"
        self.animate_dots()  # Ensure dot animation starts

    def animate_dots(self):
        """Animate dots for loading."""
        if self.upload_in_progress:  # Only animate if upload is in progress
            self.dot_label.config(text="." * (self.dot_index % 4))  # Cycle through 0 to 3 dots
            self.dot_index += 1
            self.root.after(500, self.animate_dots)  # Update every 500 milliseconds
        else:
            # Clear the dots when upload is complete or if stopped
            self.dot_label.config(text="")

    def distribute_release(self):
        """Distribute the release using the provided information."""
        file_path = self.entry_file_path.get()
        build_version = self.entry_build_version.get()
        group = self.group_var.get()

        if not file_path or not build_version:
            self.root.after(0, self.show_popup, "All fields are required.", "Error")
            self.root.after(0, self.hide_progress_elements)  # Hide progress elements if fields are missing
            return

        try:
            # New app details and token
            app_name = "karthickkumar.collegedunia-gmail.com/iOS"
            token = "8fdcda8f1e60bf37b1943ac14958dea3514e937a"
            
            command = [
                "appcenter",
                "distribute",
                "release",
                "--app", app_name,
                "--file", file_path,
                "--group", group,
                "--token", token
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)

            self.root.after(0, self.show_popup, "Release distributed successfully!", "Success")
            self.root.after(0, self.show_success_screen)  # Show success screen
        except subprocess.CalledProcessError as e:
            self.root.after(0, self.show_popup, f"An error occurred: {e}", "Error")
        finally:
            self.root.after(0, self.hide_progress_elements)  # Hide progress elements after process completes

    def show_popup(self, message, title):
        """Show a popup message."""
        messagebox.showinfo(title, message)

    def show_success_screen(self):
        """Show the success screen."""
        self.uploading_label.pack_forget()
        self.dot_label.pack_forget()
        self.progress_message.config(text="Upload successful!", fg="#008000")  # Green text
        self.progress_message.pack(pady=20)

    def show_failure_screen(self):
        """Show the failure screen."""
        self.uploading_label.pack_forget()
        self.dot_label.pack_forget()
        self.progress_message.config(text="Upload failed! Please check your network or VPN connection.", fg="#ff0000")  # Red text
        self.progress_message.pack(pady=20)

    def hide_progress_elements(self):
        """Hide the progress elements."""
        self.uploading_label.pack_forget()
        self.dot_label.pack_forget()
        self.progress_message.pack_forget()
        self.distribute_button.config(state=tk.NORMAL)  # Re-enable the button

# Create the main application window
root = tk.Tk()
app = AppCenterApp(root)
root.mainloop()
