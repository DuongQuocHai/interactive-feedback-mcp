# Interactive Feedback MCP UI (Tkinter Version)
# Developed by Fábio Ferreira (https://x.com/fabiomlferreira)
# Inspired by/related to dotcursorrules.com (https://dotcursorrules.com/)
import os
import sys
import json
import psutil
import argparse
import subprocess
import threading
import hashlib
from typing import Optional, TypedDict
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import queue
from settings_manager import SettingsManager, get_project_settings_group

class FeedbackResult(TypedDict):
    command_logs: str
    interactive_feedback: str

class FeedbackConfig(TypedDict):
    run_command: str
    execute_automatically: bool

def kill_tree(process: subprocess.Popen):
    killed: list[psutil.Process] = []
    parent = psutil.Process(process.pid)
    for proc in parent.children(recursive=True):
        try:
            proc.kill()
            killed.append(proc)
        except psutil.Error:
            pass
    try:
        parent.kill()
    except psutil.Error:
        pass
    killed.append(parent)

    # Terminate any remaining processes
    for proc in killed:
        try:
            if proc.is_running():
                proc.terminate()
        except psutil.Error:
            pass

def get_user_environment() -> dict[str, str]:
    return os.environ.copy()

def _format_windows_path(path: str) -> str:
    """Format path for Windows display"""
    if os.name == 'nt':
        # Convert forward slashes to backslashes
        path = path.replace("/", "\\")
        # Capitalize drive letter if path starts with x:\
        if len(path) >= 2 and path[1] == ":" and path[0].isalpha():
            path = path[0].upper() + path[1:]
    return path

class FeedbackUI:
    def __init__(self, project_directory: str, prompt: str):
        self.project_directory = project_directory
        self.prompt = prompt
        self.process: Optional[subprocess.Popen] = None
        self.log_buffer = []
        self.feedback_result = None
        self.log_queue = queue.Queue()
        
        # Initialize settings manager
        self.settings = SettingsManager("InteractiveFeedbackMCP", "InteractiveFeedbackMCP")
        
        # Load configuration from settings
        self._load_settings()
        
        self._create_ui()
        
        if self.config.get("execute_automatically", False):
            self._run_command()

    def _load_settings(self):
        """Load settings from storage"""
        # Load project-specific settings
        self.project_group_name = get_project_settings_group(self.project_directory)
        with self.settings.beginGroup(self.project_group_name):
            loaded_run_command = self.settings.value("run_command", "", str)
            loaded_execute_auto = self.settings.value("execute_automatically", False, bool)
            self.command_section_visible = self.settings.value("commandSectionVisible", False, bool)
        
        self.config: FeedbackConfig = {
            "run_command": loaded_run_command,
            "execute_automatically": loaded_execute_auto
        }

    def _load_window_settings(self):
        """Load window geometry and state from settings"""
        with self.settings.beginGroup("MainWindow_General"):
            geometry = self.settings.value("geometry")
            if geometry:
                self.root.geometry(geometry)
            else:
                # Default geometry and center window
                self.root.geometry("800x600")
                self.root.update_idletasks()
                x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
                y = (self.root.winfo_screenheight() // 2) - (600 // 2)
                self.root.geometry(f"800x600+{x}+{y}")
            
            state = self.settings.value("windowState")
            if state:
                # Restore window state (maximized, etc.)
                if state == "zoomed":
                    self.root.state('zoomed')

    def _create_ui(self):
        self.root = tk.Tk()
        self.root.title("Interactive Feedback MCP")
        self.root.configure(bg='#2b2b2b')
        
        # Load window geometry and state
        self._load_window_settings()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        style.configure('TEntry', fieldbackground='#404040', foreground='white')
        style.configure('TCheckbutton', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toggle Command Section Button
        self.toggle_command_button = ttk.Button(
            main_frame, 
            text="Show Command Section",
            command=self._toggle_command_section
        )
        self.toggle_command_button.pack(fill=tk.X, pady=(0, 10))
        
        # Command section
        self.command_frame = ttk.LabelFrame(main_frame, text="Command")
        self.command_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Working directory label
        formatted_path = _format_windows_path(self.project_directory)
        working_dir_label = ttk.Label(
            self.command_frame, 
            text=f"Working directory: {formatted_path}"
        )
        working_dir_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # Command input row
        command_input_frame = ttk.Frame(self.command_frame)
        command_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.command_entry = ttk.Entry(command_input_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.command_entry.bind('<Return>', lambda e: self._run_command())
        self.command_entry.bind('<KeyRelease>', lambda e: self._update_config())
        
        self.run_button = ttk.Button(
            command_input_frame, 
            text="Run",
            command=self._run_command
        )
        self.run_button.pack(side=tk.RIGHT)
        
        # Auto-execute and save config row
        config_frame = ttk.Frame(self.command_frame)
        config_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_check = ttk.Checkbutton(
            config_frame,
            text="Execute automatically on next run",
            command=self._update_config
        )
        self.auto_check.pack(side=tk.LEFT)
        
        save_button = ttk.Button(
            config_frame,
            text="Save Configuration",
            command=self._save_config
        )
        save_button.pack(side=tk.RIGHT)
        
        # Console section
        console_frame = ttk.LabelFrame(self.command_frame, text="Console")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            height=10,
            bg='#1e1e1e',
            fg='white',
            insertbackground='white',
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Clear button
        clear_button = ttk.Button(
            console_frame,
            text="Clear",
            command=self.clear_logs
        )
        clear_button.pack(anchor=tk.E, padx=5, pady=(0, 5))
        
        # Set command section visibility based on settings
        if not self.command_section_visible:
            self.command_frame.pack_forget()  # Initially hidden
            self.toggle_command_button.config(text="Show Command Section")
        else:
            self.toggle_command_button.config(text="Hide Command Section")
        
        # Feedback section
        feedback_frame = ttk.LabelFrame(main_frame, text="Feedback")
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Description label
        description_label = ttk.Label(
            feedback_frame,
            text=self.prompt,
            wraplength=750
        )
        description_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # Feedback text area
        self.feedback_text = scrolledtext.ScrolledText(
            feedback_frame,
            height=5,
            bg='#1e1e1e',
            fg='white',
            insertbackground='white',
            font=('Arial', 10)
        )
        self.feedback_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.feedback_text.insert('1.0', "Enter your feedback here...")
        self.feedback_text.bind('<Control-Return>', lambda e: self._submit_feedback())
        
        # Submit button
        submit_button = ttk.Button(
            feedback_frame,
            text="Send Feedback (Ctrl+Enter)",
            command=self._submit_feedback
        )
        submit_button.pack(anchor=tk.E, padx=5, pady=(0, 5))
        
        # Credits with clickable links
        credits_frame = ttk.Frame(main_frame)
        credits_frame.pack(anchor=tk.S, pady=(10, 0))
        
        credits_text = 'Need to improve? Contact Fábio Ferreira on '
        credits_label1 = ttk.Label(
            credits_frame,
            text=credits_text,
            font=('Arial', 8),
            foreground='#cccccc'
        )
        credits_label1.pack(side=tk.LEFT)
        
        # X.com link
        x_link = ttk.Label(
            credits_frame,
            text='X.com',
            font=('Arial', 8, 'underline'),
            foreground='#4A9EFF',
            cursor='hand2'
        )
        x_link.pack(side=tk.LEFT)
        x_link.bind('<Button-1>', lambda e: self._open_url('https://x.com/fabiomlferreira'))
        
        credits_text2 = ' or visit '
        credits_label2 = ttk.Label(
            credits_frame,
            text=credits_text2,
            font=('Arial', 8),
            foreground='#cccccc'
        )
        credits_label2.pack(side=tk.LEFT)
        
        # dotcursorrules.com link
        rules_link = ttk.Label(
            credits_frame,
            text='dotcursorrules.com',
            font=('Arial', 8, 'underline'),
            foreground='#4A9EFF',
            cursor='hand2'
        )
        rules_link.pack(side=tk.LEFT)
        rules_link.bind('<Button-1>', lambda e: self._open_url('https://dotcursorrules.com'))
        
        # Start the log processing and process monitoring
        self.root.after(100, self._process_log_queue)
        self.root.after(100, self._check_process_status)

    def _toggle_command_section(self):
        if self.command_frame.winfo_viewable():
            self.command_frame.pack_forget()
            self.toggle_command_button.config(text="Show Command Section")
        else:
            # Find the feedback frame to pack before it
            feedback_frame = None
            for child in self.root.winfo_children():
                if hasattr(child, 'winfo_children'):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ttk.LabelFrame) and grandchild.cget('text') == 'Feedback':
                            feedback_frame = grandchild
                            break
                if feedback_frame:
                    break
            
            if feedback_frame:
                self.command_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), before=feedback_frame)
            else:
                self.command_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.toggle_command_button.config(text="Hide Command Section")
        
        # Save visibility state immediately
        with self.settings.beginGroup(self.project_group_name):
            self.settings.setValue("commandSectionVisible", self.command_frame.winfo_viewable())

    def _update_config(self):
        self.config["run_command"] = self.command_entry.get()
        self.config["execute_automatically"] = self.auto_check.instate(['selected'])
        
        # Save settings in real-time
        with self.settings.beginGroup(self.project_group_name):
            self.settings.setValue("run_command", self.config["run_command"])
            self.settings.setValue("execute_automatically", self.config["execute_automatically"])

    def _append_log(self, text: str):
        self.log_buffer.append(text)
        self.log_queue.put(text)

    def _process_log_queue(self):
        try:
            while True:
                text = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, text.rstrip() + '\n')
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self._process_log_queue)

    def _check_process_status(self):
        if self.process and self.process.poll() is not None:
            exit_code = self.process.poll()
            self._append_log(f"\nProcess exited with code {exit_code}\n")
            self.run_button.config(text="Run")
            self.process = None
            self.root.focus_force()
            self.feedback_text.focus()
        
        # Schedule next check
        self.root.after(100, self._check_process_status)

    def _open_url(self, url: str):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def _run_command(self):
        if self.process:
            kill_tree(self.process)
            self.process = None
            self.run_button.config(text="Run")
            return

        self.log_buffer = []
        command = self.command_entry.get()
        if not command:
            self._append_log("Please enter a command to run\n")
            return

        self._append_log(f"$ {command}\n")
        self.run_button.config(text="Stop")

        try:
            self.process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.project_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=get_user_environment(),
                text=True,
                bufsize=1,
                encoding="utf-8",
                errors="ignore",
                close_fds=True,
            )

            def read_output(pipe):
                for line in iter(pipe.readline, ""):
                    self.log_queue.put(line)

            threading.Thread(
                target=read_output,
                args=(self.process.stdout,),
                daemon=True
            ).start()

            threading.Thread(
                target=read_output,
                args=(self.process.stderr,),
                daemon=True
            ).start()

            # Start process status checking
            self._check_process_status()

        except Exception as e:
            self._append_log(f"Error running command: {str(e)}\n")
            self.run_button.config(text="Run")

    def _submit_feedback(self):
        self.feedback_result = FeedbackResult(
            logs="".join(self.log_buffer),
            interactive_feedback=self.feedback_text.get('1.0', tk.END).strip(),
        )
        self.root.quit()

    def clear_logs(self):
        self.log_buffer = []
        self.log_text.delete('1.0', tk.END)

    def _save_config(self):
        # Save run_command and execute_automatically to settings
        with self.settings.beginGroup(self.project_group_name):
            self.settings.setValue("run_command", self.config["run_command"])
            self.settings.setValue("execute_automatically", self.config["execute_automatically"])
        self._append_log("Configuration saved for this project.\n")

    def _save_window_state(self):
        """Save window geometry and state before closing"""
        with self.settings.beginGroup("MainWindow_General"):
            # Save current geometry
            geometry = self.root.geometry()
            self.settings.setValue("geometry", geometry)
            
            # Save window state
            state = self.root.state()
            if state == "zoomed":
                self.settings.setValue("windowState", "zoomed")
            else:
                self.settings.setValue("windowState", "normal")
        
        # Save command section visibility
        with self.settings.beginGroup(self.project_group_name):
            self.settings.setValue("commandSectionVisible", self.command_frame.winfo_viewable())

    def run(self) -> FeedbackResult:
        # Bind close event to save settings
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()
        
        if self.process:
            kill_tree(self.process)

        if not self.feedback_result:
            return FeedbackResult(logs="".join(self.log_buffer), interactive_feedback="")

        return self.feedback_result

    def _on_closing(self):
        """Handle window closing event"""
        self._save_window_state()
        self.root.destroy()

def get_project_settings_group(project_dir: str) -> str:
    basename = os.path.basename(os.path.normpath(project_dir))
    full_hash = hashlib.md5(project_dir.encode('utf-8')).hexdigest()[:8]
    return f"{basename}_{full_hash}"

def feedback_ui(project_directory: str, prompt: str, output_file: Optional[str] = None) -> Optional[FeedbackResult]:
    ui = FeedbackUI(project_directory, prompt)
    result = ui.run()

    if output_file and result:
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f)
        return None

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback UI")
    parser.add_argument("--project-directory", default=os.getcwd(), help="The project directory to run the command in")
    parser.add_argument("--prompt", default="I implemented the changes you requested.", help="The prompt to show to the user")
    parser.add_argument("--output-file", help="Path to save the feedback result as JSON")
    args = parser.parse_args()

    result = feedback_ui(args.project_directory, args.prompt, args.output_file)
    if result:
        print(f"\nLogs collected: \n{result['logs']}")
        print(f"\nFeedback received:\n{result['interactive_feedback']}")
    sys.exit(0)
