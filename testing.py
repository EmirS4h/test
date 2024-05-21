import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading
import keyboard
import my_conn
import sys


# GUI class for the auto clicker application
class ClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        self.running = False
        # Game stats
        self.games = {
            "TapSwap": {
                "energy": 0,
                "max_energy": 0,
                "damage": 0,
                "recharge_speed": 0,
                "last_checked": time.time(),
            },
            "MemeFi": {
                "energy": 0,
                "max_energy": 0,
                "damage": 0,
                "recharge_speed": 0,
                "last_checked": time.time(),
            },
            "Hamster": {
                "energy": 0,
                "max_energy": 0,
                "damage": 0,
                "recharge_speed": 0,
                "last_checked": time.time(),
            },
        }
        self.current_game = "TapSwap"  # Start with TapSwap
        self.image_paths = {
            "TapSwap": ["tapswap.png", "tapswapStart.png", "tapswapClose.png"],
            "MemeFi": ["memefi.png", "memefiStart.png"],
            "Hamster": ["hamster.png", "hamsterStart.png", "hamsterCollect.png"],
            "CloseTapSwap": "tapswapCloseButton.png",
            "CloseMemeFi": "memefiCloseButton.png",
            "CloseHamster": "hamsterCloseButton.png",
            "Exit": "exit.png",
            "Exit2": "exit2.png",
        }

        # Create widgets for the GUI
        self.create_widgets()

    def create_widgets(self):
        my_conn.add_user()
        row = 0

        # Parameters for TapSwap
        tk.Label(self.root, text="TapSwap Energy Cap:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.tapswap_energy_cap = tk.Entry(self.root)
        self.tapswap_energy_cap.grid(row=row, column=1, padx=10, pady=10)
        row += 1
        self.tapswap_energy_label = tk.Label(self.root, text="Current Energy: 0")
        self.tapswap_energy_label.grid(
            row=row, column=0, columnspan=2, padx=10, pady=10
        )
        row += 1

        tk.Label(self.root, text="TapSwap Damage:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.tapswap_damage = tk.Entry(self.root)
        self.tapswap_damage.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        tk.Label(self.root, text="TapSwap Recharging Speed:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.tapswap_recharge_speed = tk.Entry(self.root)
        self.tapswap_recharge_speed.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Parameters for MemeFi
        tk.Label(self.root, text="MemeFi Energy Cap:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.memefi_energy_cap = tk.Entry(self.root)
        self.memefi_energy_cap.grid(row=row, column=1, padx=10, pady=10)
        row += 1
        self.memefi_energy_label = tk.Label(self.root, text="Current Energy: 0")
        self.memefi_energy_label.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        row += 1

        tk.Label(self.root, text="MemeFi Damage:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.memefi_damage = tk.Entry(self.root)
        self.memefi_damage.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        tk.Label(self.root, text="MemeFi Recharging Speed:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.memefi_recharge_speed = tk.Entry(self.root)
        self.memefi_recharge_speed.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Parameters for Hamster
        tk.Label(self.root, text="Hamster Energy Cap:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.hamster_energy_cap = tk.Entry(self.root)
        self.hamster_energy_cap.grid(row=row, column=1, padx=10, pady=10)
        row += 1
        self.hamster_energy_label = tk.Label(self.root, text="Current Energy: 0")
        self.hamster_energy_label.grid(
            row=row, column=0, columnspan=2, padx=10, pady=10
        )
        row += 1

        tk.Label(self.root, text="Hamster Damage:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.hamster_damage = tk.Entry(self.root)
        self.hamster_damage.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        tk.Label(self.root, text="Hamster Recharging Speed:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.hamster_recharge_speed = tk.Entry(self.root)
        self.hamster_recharge_speed.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # Common parameters
        tk.Label(self.root, text="Click Delay (seconds):").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.click_delay_entry = tk.Entry(self.root)
        self.click_delay_entry.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        self.start_button = tk.Button(
            self.root, text="Start", command=self.start_clicking
        )
        self.start_button.grid(row=row, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_clicking)
        self.stop_button.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        tk.Label(self.root, text="Stop Hotkey:").grid(
            row=row, column=0, padx=10, pady=10
        )
        self.hotkey_entry = tk.Entry(self.root)
        self.hotkey_entry.grid(row=row, column=1, padx=10, pady=10)
        self.hotkey_entry.insert(0, "q")  # Default hotkey
        row += 1

        self.status_label = tk.Label(self.root, text="Status: Idle")
        self.status_label.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        row += 1

        self.energy_label = tk.Label(self.root, text="Current Game Energy: 0")
        self.energy_label.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        row += 1

    def start_clicking(self):
        try:
            # Get user input for game parameters
            self.games["TapSwap"]["max_energy"] = int(self.tapswap_energy_cap.get())
            self.games["TapSwap"]["damage"] = int(self.tapswap_damage.get())
            self.games["TapSwap"]["recharge_speed"] = float(
                self.tapswap_recharge_speed.get()
            )

            self.games["MemeFi"]["max_energy"] = int(self.memefi_energy_cap.get())
            self.games["MemeFi"]["damage"] = int(self.memefi_damage.get())
            self.games["MemeFi"]["recharge_speed"] = float(
                self.memefi_recharge_speed.get()
            )

            self.games["Hamster"]["max_energy"] = int(self.hamster_energy_cap.get())
            self.games["Hamster"]["damage"] = int(self.hamster_damage.get())
            self.games["Hamster"]["recharge_speed"] = float(
                self.hamster_recharge_speed.get()
            )

            self.click_delay = float(self.click_delay_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Please enter valid numbers for all fields.",
            )
            return

        self.running = True

        # Initialize game energy and timestamp
        for game in self.games:
            self.games[game]["energy"] = self.games[game]["max_energy"]
            self.games[game]["last_checked"] = time.time()

        self.status_label.config(text="Status: Running")

        # Start clicking and monitoring threads
        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.start()

        self.monitor_thread = threading.Thread(target=self.monitor_stop)
        self.monitor_thread.start()

        self.energy_thread = threading.Thread(target=self.energy_replenishment_loop)
        self.energy_thread.start()

    def stop_clicking(self):
        self.running = False
        self.status_label.config(text="Status: Stopped")

    def click_middle(self):
        # Click in the middle of the screen
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)

    def replenish_energy(self, game):
        # Calculate energy replenishment based on elapsed time
        current_time = time.time()
        elapsed_time = current_time - self.games[game]["last_checked"]
        replenished_energy = elapsed_time * self.games[game]["recharge_speed"]
        self.games[game]["energy"] = min(
            self.games[game]["max_energy"],
            self.games[game]["energy"] + replenished_energy,
        )
        self.games[game]["last_checked"] = current_time

    def update_energy_labels(self):
        # Update energy labels for all games
        self.tapswap_energy_label.config(
            text=f"Current Energy: {int(self.games['TapSwap']['energy'])}"
        )
        self.memefi_energy_label.config(
            text=f"Current Energy: {int(self.games['MemeFi']['energy'])}"
        )
        self.hamster_energy_label.config(
            text=f"Current Energy: {int(self.games['Hamster']['energy'])}"
        )
        self.energy_label.config(
            text=f"Current Game Energy: {int(self.games[self.current_game]['energy'])}"
        )

    def energy_replenishment_loop(self):
        while True:
            for game in self.games:
                self.replenish_energy(game)
            self.update_energy_labels()
            time.sleep(1)  # Update every second

    def click_loop(self):
        while self.running:
            # Only start clicking if the current energy is equal to the max energy
            if (
                self.games[self.current_game]["energy"]
                == self.games[self.current_game]["max_energy"]
            ):
                self.status_label.config(text=f"Status: Clicking {self.current_game}")
                # if not gw.getWindowsWithTitle("BlueStacks App Player")[0].isMaximized:
                # gw.getWindowsWithTitle("BlueStacks App Player")[0].restore()
                while self.games[self.current_game]["energy"] > 0 and self.running:
                    self.click_middle()
                    self.games[self.current_game]["energy"] -= self.games[
                        self.current_game
                    ]["damage"]
                    self.update_energy_labels()
                    time.sleep(self.click_delay)
                self.status_label.config(
                    text=f"Status: Switching from {self.current_game}"
                )
                self.switch_game()
            else:
                self.status_label.config(
                    text=f"Status: Waiting for energy {self.current_game}"
                )
                # if gw.getWindowsWithTitle("BlueStacks App Player")[0].isMaximized:
                # gw.getWindowsWithTitle("BlueStacks App Player")[0].minimize()
                time.sleep(1)

    def switch_game(self):
        # Exit the current game
        time.sleep(3)
        self.click_image(self.image_paths["Exit"])
        time.sleep(2)  # Ensure there's enough time to exit

        # Handle the special TapSwap close popup
        if self.current_game == "TapSwap":
            try:
                self.click_image(self.image_paths["TapSwap"][2])
            except:
                print("Soktuğumun pop-up ı çıkmadı")
            time.sleep(3)
            try:
                self.click_image(self.image_paths["Exit2"])
            except:
                print("2. Çıkışa gerek kalmadı galiba,sanırım,bilmiyorum.... sikicem")
            time.sleep(2)

        # Switch to the next game in the sequence
        if self.current_game == "TapSwap":
            self.current_game = "MemeFi"
        elif self.current_game == "MemeFi":
            self.current_game = "Hamster"
        else:  # self.current_game == "Hamster"
            self.current_game = self.get_next_game_with_energy()

        # Click to navigate to the selected game
        self.click_image(self.image_paths[self.current_game][0])
        time.sleep(5)
        self.click_image(self.image_paths[self.current_game][1])
        time.sleep(5)

        # Special case for Hamster game to collect coins
        if self.current_game == "Hamster":
            try:
                self.click_image(self.image_paths["Hamster"][2])
            except:
                print("Amına kodumun hamsterına girilmiyor!")
            time.sleep(5)

        self.status_label.config(text=f"Status: Running {self.current_game}")

    def get_next_game_with_energy(self):
        # Get the next game with the highest energy
        max_energy_game = max(self.games, key=lambda g: self.games[g]["energy"])
        return (
            max_energy_game if self.games[max_energy_game]["energy"] > 0 else "TapSwap"
        )

    def click_image(self, image_path):
        # Locate and click the image on screen
        try:
            location = pyautogui.locateOnScreen(image_path)
        except:
            on_closing()
            sys.exit()
        if location:
            pyautogui.click(location)
            time.sleep(5)  # Ensure sufficient delay after clicking
        else:
            self.status_label.config(text=f"Status: Failed to find {image_path}")

    def monitor_stop(self):
        # Monitor for the stop hotkey
        stop_hotkey = self.hotkey_entry.get()
        while self.running:
            if keyboard.is_pressed(stop_hotkey):
                self.stop_clicking()
                break
            time.sleep(0.1)  # Check every 0.1 seconds for better responsiveness


def on_closing():
    my_conn.remove_user()
    root.destroy()


# Main application
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
app = ClickerApp(root)
root.mainloop()
