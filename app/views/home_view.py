import tkinter as tk
import time

from tkinter import ttk, filedialog
from PIL import Image
from pathlib import Path

CHANNELS = ("r", "g", "b", "a")


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # Configure main grid
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Shared padding vars
        short_padding = (0, 10)
        tall_padding = (0, 20)
        left_padding = (10, 0)

        # ---------------- Title ----------------
        ttk.Label(
            self,
            text="Texture Packer",
            font=("Segoe UI", 20),
            anchor="w",
            wraplength=600,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=short_padding)

        # ---------------- Side-by-Side Areas ----------------
        working_frame = ttk.Frame(self)
        working_frame.grid(
            row=1, column=0, columnspan=2, sticky="nsew", pady=tall_padding
        )
        working_frame.columnconfigure(0, weight=1)
        working_frame.columnconfigure(1, weight=1)
        working_frame.rowconfigure(0, weight=1)

        # Unpack Frame
        unpack_frame = ttk.Frame(working_frame)
        unpack_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 25))
        unpack_frame.columnconfigure(0, weight=1)
        unpack_frame.columnconfigure(1, weight=1)

        ttk.Label(
            unpack_frame,
            text="Unpack Input",
            anchor="w",
            wraplength=600,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=short_padding)

        self.unpack_path = tk.StringVar()
        ttk.Button(
            unpack_frame, text="Select Input Path", command=self.select_unpack_path
        ).grid(row=1, column=0, sticky="ew", pady=tall_padding)
        ttk.Entry(unpack_frame, textvariable=self.unpack_path).grid(
            row=1, column=1, sticky="ew", padx=left_padding, pady=tall_padding
        )

        ttk.Label(
            unpack_frame,
            text="Unpack Output:",
            anchor="w",
            wraplength=600,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=short_padding)

        # Output RGBA Paths
        self.unpack_path_inputs = {}  # keys: 'r', 'g', 'b', 'a'

        # Build the paths for each channel
        for i, channel in enumerate(CHANNELS, start=2):
            var = tk.StringVar()
            self.unpack_path_inputs[channel] = var

            ttk.Label(
                unpack_frame,
                text=f"Unpack Output ({channel.capitalize()})",
                anchor="w",
                wraplength=600,
            ).grid(row=i, column=0, sticky="ew", pady=short_padding)
            ttk.Label(
                unpack_frame,
                textvariable=self.unpack_path_inputs[channel],
                anchor="e",
                wraplength=600,
            ).grid(row=i, column=1, sticky="ew", pady=short_padding)

        # Unpack button
        ttk.Button(unpack_frame, text="Unpack", command=self.unpack_channels).grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=tall_padding
        )

        # Pack Frame
        pack_frame = ttk.Frame(working_frame)
        pack_frame.grid(row=0, column=1, sticky="nsew", padx=(25, 5))
        pack_frame.columnconfigure(0, weight=1)
        pack_frame.columnconfigure(1, weight=1)

        ttk.Label(
            pack_frame,
            text="Pack Input",
            anchor="w",
            wraplength=600,
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=short_padding)

        # Input RGBA Paths
        self.pack_path_inputs = {}  # keys: 'r', 'g', 'b', 'a'

        for i, channel in enumerate(CHANNELS, start=1):
            # Create a StringVar for this channel
            var = tk.StringVar()
            self.pack_path_inputs[channel] = var

            # Button to select the file path
            ttk.Button(
                pack_frame,
                text=f"Select Input Path ({channel.capitalize()})",
                command=lambda c=channel: self.select_pack_path(c),
            ).grid(row=i, column=0, sticky="ew", pady=short_padding)

            # Entry showing the path
            ttk.Entry(pack_frame, textvariable=var).grid(
                row=i, column=1, sticky="ew", padx=left_padding, pady=short_padding
            )
            
        # Pack button
        ttk.Button(pack_frame, text="Pack", command=self.pack_channels).grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=tall_padding
        )

        # ---------------- Output log ----------------
        ttk.Label(self, text="Output Log:").grid(row=2, column=0, sticky="w")
        self.log_text_area = tk.Text(self, wrap="word", state="disabled")
        self.log_text_area.grid(row=3, column=0, columnspan=2, sticky="nsew")

    def select_unpack_path(self):
        file_path = filedialog.askopenfilename(
            title="Select a file to unpack", filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            self.log("No file selected.")
            return

        self.log(f"Opened {file_path}")

        # Loop through the dictionary and set each channel's output path
        filenames = generate_channel_filenames(Path(file_path))
        for channel in CHANNELS:
            output_filename = filenames[channel]
            self.unpack_path_inputs[channel].set(output_filename)
            self.log(f"Set {channel.upper()} channel output: {output_filename}")

        self.unpack_path.set(file_path)

    def select_pack_path(self, channel):
        file_path = filedialog.askopenfilename(
            title=f"Select {channel} channel file", filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            self.log("No file selected for packing")
            return

        self.pack_path_inputs[channel].set(file_path)
        self.log(f"Set {channel} channel path: {file_path}")

    def unpack_channels(self):
        file_path = self.unpack_path.get()

        if not file_path:
            self.log("Please select an image to unpack")
            return

        try:
            # Open the image and ensure it has an alpha channel
            with Image.open(file_path) as img:
                img = img.convert("RGBA")
                channels = dict(zip(CHANNELS, img.split()))
        except Exception as e:
            self.log(f"Failed to open image: {e}")
            return

        # Generate filenames and set the StringVars dynamically
        filenames = generate_channel_filenames(Path(file_path))

        for channel, img_obj in channels.items():
            output_filename = filenames[channel]
            img_obj.save(output_filename)
            self.unpack_path_inputs[channel].set(output_filename)
            self.log(f"Saved {channel.upper()} channel: {output_filename}")

        self.log("Unpacking complete!")

    def pack_channels(self):
        files = [self.pack_path_inputs[c].get() for c in CHANNELS]

        # Make sure all paths are set
        if not all(files):
            self.log("Please select all 4 channel files before packing")
            return

        file_path = filedialog.asksaveasfilename(
            title=f"Select output (RGBA) file name file",
            filetypes=[("PNG files", "*.png")],
        )

        if not file_path:
            self.log("No file selected for packing")
            return

        try:
            # Open each file and convert to grayscale ('L')
            channels = []
            for f in files:
                with Image.open(f) as img:
                    channels.append(img.convert("L"))

            sizes = [img.size for img in channels]
            if len(set(sizes)) != 1:
                self.log("All channel images must be the same dimensions")
                return

            # Merge into a single RGBA image
            merged = Image.merge("RGBA", channels)
            output_file = Path(file_path).with_suffix(".png")

            merged.save(output_file)
            self.log(f"Packed channels into {output_file}!")
        except Exception as e:
            self.log(f"Failed to pack channels: {e}")

    def log(self, message):
        self.log_text_area.configure(state="normal")
        self.log_text_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text_area.see(tk.END)
        self.log_text_area.configure(state="disabled")


def generate_channel_filenames(path: Path):
    return {c: f"{path.stem}_{c}{path.suffix}" for c in CHANNELS}
