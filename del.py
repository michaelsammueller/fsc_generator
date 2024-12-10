import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import paramiko
from threading import Thread


def search_and_delete_remotely_ssh(host, username, password, keywords):
    """
    Connects to a remote machine using SSH and deletes .exe files or folders
    with names containing specified keywords.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        for keyword in keywords:
            search_command = f"find / -type f -name '*{keyword}*.exe' 2>/dev/null"
            stdin, stdout, stderr = client.exec_command(search_command)
            files_to_delete = stdout.read().decode().splitlines()

            search_command_dir = f"find / -type d -name '*{keyword}*' 2>/dev/null"
            stdin, stdout, stderr = client.exec_command(search_command_dir)
            directories_to_delete = stdout.read().decode().splitlines()

            items_to_delete = files_to_delete + directories_to_delete

            for item in items_to_delete:
                delete_command = f"rm -rf '{item}'"
                client.exec_command(delete_command)
        
        client.close()
        return True
    except Exception:
        return False


def search_and_delete_remotely_psexec(host, username, password, keywords):
    """
    Connects to a remote machine using psexec and deletes .exe files or folders
    with names containing specified keywords.
    """
    try:
        for keyword in keywords:
            search_command = (
                f'psexec \\\\{host} -u {username} -p {password} '
                f'"cmd /c forfiles /P C:\\ /S /M *{keyword}*.exe /C \"cmd /c del @path /Q\" 2>nul"'
            )
            subprocess.run(search_command, shell=True, check=True)

            search_command_dir = (
                f'psexec \\\\{host} -u {username} -p {password} '
                f'"cmd /c for /D %%d in (C:\\*{keyword}*) do rd /S /Q %%d"'
            )
            subprocess.run(search_command_dir, shell=True, check=True)

        return True
    except subprocess.CalledProcessError:
        return False


def process_machines(keywords, progress_bar, progress_label, on_complete):
    username = "Best"
    password = "best"
    remote_machines = [ 
        {"host": "PILOT01", "username": username, "password": password},
        {"host": "PILOT01-360", "username": username, "password": password},
        {"host": "PILOT02", "username": username, "password": password},
        {"host": "PILOT02-360", "username": username, "password": password},
        {"host": "PILOT03", "username": username, "password": password},
        {"host": "PILOT03-360", "username": username, "password": password},
        {"host": "PILOT04", "username": username, "password": password},
        {"host": "PILOT04-360", "username": username, "password": password},
        {"host": "PILOT05", "username": username, "password": password},
        {"host": "PILOT05-360", "username": username, "password": password},
        {"host": "PILOT06", "username": username, "password": password},
        {"host": "PILOT06-360", "username": username, "password": password},
        {"host": "PILOT07", "username": username, "password": password},
        {"host": "PILOT07-360", "username": username, "password": password},
        {"host": "PILOT08", "username": username, "password": password},
        {"host": "PILOT08-360", "username": username, "password": password},
        {"host": "PILOT09", "username": username, "password": password},
        {"host": "PILOT09-360", "username": username, "password": password},
        {"host": "PILOT10", "username": username, "password": password},
        {"host": "PILOT10-360", "username": username, "password": password},
        {"host": "PILOT11", "username": username, "password": password},
        {"host": "PILOT11-360", "username": username, "password": password},
        {"host": "PILOT12", "username": username, "password": password},
        {"host": "PILOT12-360", "username": username, "password": password},
        {"host": "BCO01", "username": username, "password": password},
        {"host": "BCO02", "username": username, "password": password},
        {"host": "BCO03", "username": username, "password": password},
        {"host": "BCO04", "username": username, "password": password},
        {"host": "BCO05", "username": username, "password": password},
        {"host": "BCO06", "username": username, "password": password},
        {"host": "BIM01", "username": username, "password": password},
        {"host": "RCTRL01", "username": username, "password": password},
        {"host": "RCTRL02", "username": username, "password": password},
        {"host": "RCTRL03", "username": username, "password": password},
        {"host": "RCTRL04", "username": username, "password": password},
        {"host": "RCTRL05", "username": username, "password": password},
        {"host": "RCTRL06", "username": username, "password": password},
        {"host": "RCTRL07", "username": username, "password": password},
        {"host": "RCTRL08", "username": username, "password": password},
        {"host": "RCTRL09", "username": username, "password": password},
        {"host": "RCTRL10", "username": username, "password": password},
        {"host": "RCTRL11", "username": username, "password": password},
        {"host": "RCTRL12", "username": username, "password": password},
        {"host": "CON01", "username": username, "password": password},
        {"host": "CON02", "username": username, "password": password},
        {"host": "TWRSUP-360", "username": username, "password": password},
        {"host": "CLEARANCE-360", "username": username, "password": password},
        {"host": "GRNDCTRL01-360", "username": username, "password": password},
        {"host": "GRNDCTRL02-360", "username": username, "password": password},
        {"host": "TWRCNTL01-360", "username": username, "password": password},
        {"host": "TWRCTRL02-360", "username": username, "password": password},
        {"host": "GRNDCTRL01-360", "username": username, "password": password},
        {"host": "GRNDCTRL02-360", "username": username, "password": password},
        {"host": "SYSMAN-360", "username": username, "password": password},
        {"host": "STBY-SYSMAN-360", "username": username, "password": password},
        {"host": "FAB01", "username": username, "password": password},
        {"host": "FAB02", "username": username, "password": password},
        {"host": "BSM01", "username": username, "password": password}
    ]  # Same as in your list above

    total = len(remote_machines)
    for i, machine in enumerate(remote_machines, start=1):
        success = search_and_delete_remotely_ssh(
            machine["host"], username, password, keywords
        )
        if not success:
            search_and_delete_remotely_psexec(
                machine["host"], username, password, keywords
            )

        progress_bar["value"] = (i / total) * 100
        progress_label["text"] = f"Processing {i}/{total} machines..."
    
    on_complete()


def start_update(root, keywords, progress_bar, progress_label):
    def on_complete():
        progress_label["text"] = "Update completed successfully!"
        messagebox.showinfo("HackerPrep2.1 Update Utility", "Update completed successfully!")
        root.destroy()

    Thread(
        target=process_machines,
        args=(keywords, progress_bar, progress_label, on_complete),
        daemon=True,
    ).start()


def create_gui():
    keywords = ["Waker", "Sauerkraut", "HackerPrep", "Hafaza"]

    root = tk.Tk()
    root.title("HackerPrep2.1 Update Utility")
    root.geometry("400x300")

    # License Agreement
    license_text = tk.Text(root, wrap="word", height=10, width=50)
    license_text_content = """
            HACKERPREP 2.1 UPDATE UTILITY SOFTWARE LICENSE AGREEMENT

            PLEASE READ THIS LICENSE AGREEMENT CAREFULLY BEFORE USING THIS SOFTWARE.

            This License Agreement ("Agreement") is a binding legal contract between you ("User") and the provider of the HackerPrep 2.1 Update Utility software ("Licensor"). By clicking "I Agree" or using the software, you accept and agree to be bound by the terms of this Agreement. If you do not agree to these terms, you must not use the software.

            1. LICENSE GRANT
            The Licensor hereby grants the User a non-exclusive, non-transferable, revocable license to use the HackerPrep 2.1 Update Utility software ("Software") solely for updating systems within your authorized network as described in this Agreement.

            2. USE RESTRICTIONS
            The User shall not:
            - Modify, decompile, reverse-engineer, or disassemble the Software.
            - Distribute, sell, sublicense, or lease the Software to any third party.
            - Use the Software for any illegal or unauthorized purpose.

            3. UPDATES AND REMOVALS
            As part of the Software’s operation, the User acknowledges and agrees that:
            - The Software will scan all machines in the network as defined by the User’s provided list.
            - The Software will identify and remove all products or components labeled as "Hafaza," including but not limited to Hafaza-related executables, files, directories, or associated configurations.
            - The User has reviewed and understands the impact of these actions on the network systems before proceeding with the update.

            4. DISCLAIMER OF WARRANTIES
            The Software is provided "as is" and without any warranties of any kind, either express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement. The Licensor does not warrant that the Software will meet your requirements, operate uninterrupted, or be error-free.

            5. LIMITATION OF LIABILITY
            In no event shall the Licensor be liable for any indirect, incidental, consequential, special, or exemplary damages arising out of or in connection with the use of the Software, including but not limited to loss of data, loss of profits, or system downtime, even if the Licensor has been advised of the possibility of such damages.

            6. USER RESPONSIBILITIES
            The User is solely responsible for:
            - Ensuring all systems in the network are appropriately backed up prior to using the Software.
            - Reviewing and approving the removal of Hafaza products as part of the update process.
            - Any consequences arising from the Software’s execution within the User's network.

            7. TERMINATION
            This Agreement is effective until terminated. The Licensor may terminate this Agreement at any time if the User breaches any term of this Agreement. Upon termination, the User must cease all use of the Software and destroy all copies in their possession.

            8. GOVERNING LAW
            This Agreement shall be governed by and construed in accordance with the laws of [Your Jurisdiction], without regard to its conflict of law provisions.

            9. ACCEPTANCE OF TERMS
            By clicking "I Agree" or using the Software, you confirm that you have read and understood this Agreement and agree to be bound by its terms. You also acknowledge that all Hafaza products will be removed from machines in the network as part of the update process.

            If you have any questions or concerns about this Agreement, please contact [Support Contact Information].
        """
    license_text.insert("1.0", license_text_content)

    license_text.config(state="disabled")
    license_text.pack(pady=10)

    agree_var = tk.IntVar()
    agree_check = tk.Checkbutton(root, text="I agree to the terms", variable=agree_var)
    agree_check.pack()

    # Progress bar
    progress_label = tk.Label(root, text="Ready to start.")
    progress_label.pack(pady=5)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # Start Button
    def on_start():
        if agree_var.get() == 0:
            messagebox.showerror("Error", "You must accept the license agreement to proceed.")
            return

        progress_label["text"] = "Starting update..."
        start_update(root, keywords, progress_bar, progress_label)

    start_button = tk.Button(root, text="Start Update", command=on_start)
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()