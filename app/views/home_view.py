import tkinter as tk
import time
import customtkinter as ctk

from tkinter import filedialog
from tkinterdnd2 import DND_FILES
from PIL import Image, ImageOps
from pathlib import Path

CHANNELS = ("r", "g", "b", "a")

CHANNEL_COLORS = {
    "r": "#c0392b",
    "g": "#27ae60",
    "b": "#2980b9",
    "a": "#7f8c8d",
}

BG_APP      = "#1c1c1c"
BG_PANEL    = "#242424"
BG_ENTRY    = "#2a2a2a"
BG_PREVIEW  = "#1a1a1a"
BG_LOG      = "#181818"
BORDER      = "#3a3a3a"
BORDER_DND  = "#3a7bd5"
FG_MAIN     = "#e0e0e0"
FG_SUB      = "#a0a0a0"
FG_DIM      = "#666666"
BTN_BLUE    = "#3a7bd5"
BTN_SEC     = "#2e2e2e"
BTN_UNPACK  = "#5a3a9a"
BTN_PACK    = "#2e7d52"

PREVIEW_W = 440
PREVIEW_H = 140
THUMB_SIZE = 44


def _parse_drop_path(data: str) -> str:
    """Extract a single file path from a tkinterdnd2 drop event data string."""
    data = data.strip()
    if data.startswith("{"):
        return data[1:data.index("}")]
    return data.split()[0]


class HomeView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_APP)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="Texture Packer",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=FG_MAIN,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 10))

        # Two-panel working area
        working_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        working_frame.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        working_frame.grid_columnconfigure(0, weight=1)
        working_frame.grid_columnconfigure(1, weight=1)
        working_frame.grid_rowconfigure(0, weight=1)

        self._build_unpack_panel(working_frame)
        self._build_pack_panel(working_frame)

        # Log
        self._build_log()

    # ── Image helpers ──────────────────────────────────────────────────────────

    def _make_preview(self, pil_image: Image.Image) -> ctk.CTkImage:
        """Resize and crop a PIL image to fill the main preview area."""
        img = ImageOps.fit(pil_image.copy().convert("RGB"), (PREVIEW_W, PREVIEW_H), Image.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(PREVIEW_W, PREVIEW_H))

    def _make_thumb(self, pil_image: Image.Image) -> ctk.CTkImage:
        """Resize and crop a PIL image to a square thumbnail."""
        img = ImageOps.fit(pil_image.copy().convert("RGB"), (THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(THUMB_SIZE, THUMB_SIZE))

    def _preview_label(self, parent) -> tuple[ctk.CTkFrame, ctk.CTkLabel]:
        """Create a fixed-size preview container and the inner label for image updates."""
        container = ctk.CTkFrame(
            parent, fg_color=BG_PREVIEW, corner_radius=8, height=PREVIEW_H,
        )
        container.grid_propagate(False)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        label = ctk.CTkLabel(
            container,
            text="No image loaded",
            font=ctk.CTkFont(size=12),
            text_color="#3a3a3a",
            fg_color="transparent",
        )
        label.grid(row=0, column=0, sticky="nsew")
        return container, label

    def _thumb_label(self, parent) -> ctk.CTkLabel:
        """Create a blank thumbnail label."""
        return ctk.CTkLabel(
            parent,
            text="",
            fg_color=BG_PREVIEW,
            width=THUMB_SIZE,
            height=THUMB_SIZE,
            corner_radius=6,
        )

    # ── DnD ───────────────────────────────────────────────────────────────────

    def _register_dnd(self, ctk_entry: ctk.CTkEntry, callback):
        """Register drag-and-drop on a CTkEntry with border highlight feedback."""
        inner = ctk_entry._entry
        inner.drop_target_register(DND_FILES)
        inner.dnd_bind("<<DragEnter>>", lambda e: ctk_entry.configure(border_color=BORDER_DND))
        inner.dnd_bind("<<DragLeave>>", lambda e: ctk_entry.configure(border_color=BORDER))

        def on_drop(e, entry=ctk_entry, cb=callback):
            entry.configure(border_color=BORDER)
            cb(_parse_drop_path(e.data))

        inner.dnd_bind("<<Drop>>", on_drop)

    # ── Panel builders ────────────────────────────────────────────────────────

    def _build_unpack_panel(self, parent):
        panel = ctk.CTkFrame(
            parent, fg_color=BG_PANEL, corner_radius=10,
            border_width=1, border_color=BORDER,
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        panel.grid_columnconfigure(0, weight=1)

        row = 0

        ctk.CTkLabel(
            panel, text="UNPACK",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=FG_SUB, anchor="w",
        ).grid(row=row, column=0, sticky="ew", padx=18, pady=(16, 10))
        row += 1

        # Input file row
        input_row = ctk.CTkFrame(panel, fg_color="transparent")
        input_row.grid(row=row, column=0, sticky="ew", padx=18, pady=(0, 10))
        input_row.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            input_row, text="Select Input",
            fg_color=BTN_BLUE, hover_color="#4a8be5",
            font=ctk.CTkFont(size=13), height=34,
            command=self.select_unpack_path,
        ).grid(row=0, column=0)

        self.unpack_path = tk.StringVar()
        unpack_entry = ctk.CTkEntry(
            input_row, textvariable=self.unpack_path,
            fg_color=BG_ENTRY, border_color=BORDER,
            text_color="#bbbbbb", height=34,
            placeholder_text="No file selected…",
        )
        unpack_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self._register_dnd(unpack_entry, self._load_unpack_path)
        row += 1

        # Source image preview
        _container, self.unpack_preview = self._preview_label(panel)
        _container.grid(row=row, column=0, sticky="ew", padx=18, pady=(0, 10))
        row += 1

        # Divider
        ctk.CTkFrame(panel, height=1, fg_color="#2a2a2a").grid(
            row=row, column=0, sticky="ew", padx=18, pady=8,
        )
        row += 1

        ctk.CTkLabel(
            panel, text="Output channels  (auto-generated from input path)",
            font=ctk.CTkFont(size=11),
            text_color=FG_DIM, anchor="w",
        ).grid(row=row, column=0, sticky="ew", padx=18, pady=(0, 8))
        row += 1

        self.unpack_path_inputs = {}
        self.unpack_thumbs = {}
        for channel in CHANNELS:
            var = tk.StringVar()
            self.unpack_path_inputs[channel] = var
            self.unpack_thumbs[channel] = self._channel_row(
                panel, row, channel, var, show_thumb=True,
            )
            row += 1

        ctk.CTkButton(
            panel, text="Unpack Channels",
            fg_color=BTN_UNPACK, hover_color="#6a4aaa",
            font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=self.unpack_channels,
        ).grid(row=row, column=0, sticky="ew", padx=18, pady=(12, 18))

    def _build_pack_panel(self, parent):
        panel = ctk.CTkFrame(
            parent, fg_color=BG_PANEL, corner_radius=10,
            border_width=1, border_color=BORDER,
        )
        panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        panel.grid_columnconfigure(0, weight=1)

        row = 0

        ctk.CTkLabel(
            panel, text="PACK",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=FG_SUB, anchor="w",
        ).grid(row=row, column=0, sticky="ew", padx=18, pady=(16, 10))
        row += 1

        self.pack_path_inputs = {}
        self.pack_thumbs = {}
        for channel in CHANNELS:
            var = tk.StringVar()
            self.pack_path_inputs[channel] = var
            self.pack_thumbs[channel] = self._channel_row(
                panel, row, channel, var,
                browse_cmd=lambda c=channel: self.select_pack_path(c),
                drop_cmd=lambda path, c=channel: self._load_pack_path(c, path),
                show_thumb=True,
            )
            row += 1

        # Result preview
        _container, self.pack_preview = self._preview_label(panel)
        _container.grid(row=row, column=0, sticky="ew", padx=18, pady=(8, 10))
        row += 1

        ctk.CTkButton(
            panel, text="Pack into RGBA",
            fg_color=BTN_PACK, hover_color="#38956a",
            font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=self.pack_channels,
        ).grid(row=row, column=0, sticky="ew", padx=18, pady=(0, 18))

    def _channel_row(
        self, parent, row, channel, var,
        browse_cmd=None, drop_cmd=None, show_thumb=False,
    ) -> ctk.CTkLabel | None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=18, pady=4)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text=channel.upper(),
            fg_color=CHANNEL_COLORS[channel], text_color="#ffffff",
            font=ctk.CTkFont(size=11, weight="bold"),
            width=28, height=28, corner_radius=6,
        ).grid(row=0, column=0, padx=(0, 10))

        entry = ctk.CTkEntry(
            frame, textvariable=var,
            fg_color=BG_ENTRY, border_color=BORDER,
            text_color="#bbbbbb", height=32,
            placeholder_text="No file selected…",
        )
        entry.grid(row=0, column=1, sticky="ew")

        if drop_cmd:
            self._register_dnd(entry, drop_cmd)

        col = 2
        if browse_cmd:
            ctk.CTkButton(
                frame, text="Browse",
                fg_color=BTN_SEC, hover_color="#383838",
                border_width=1, border_color=BORDER,
                text_color="#cccccc",
                font=ctk.CTkFont(size=12), height=32, width=70,
                command=browse_cmd,
            ).grid(row=0, column=col, padx=(10, 0))
            col += 1

        thumb = None
        if show_thumb:
            thumb = self._thumb_label(frame)
            thumb.grid(row=0, column=col, padx=(10, 0))

        return thumb

    # ── Log ───────────────────────────────────────────────────────────────────

    def _build_log(self):
        log_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        log_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 20))
        log_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            log_frame, text="OUTPUT LOG",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=FG_DIM, anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            height=120,
            fg_color=BG_LOG,
            border_color=BORDER,
            border_width=1,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#888888",
            state="disabled",
        )
        self.log_textbox.grid(row=1, column=0, sticky="ew")

        tb = self.log_textbox._textbox
        tb.tag_configure("time", foreground="#555555")
        tb.tag_configure("ok",   foreground="#27ae60")
        tb.tag_configure("info", foreground="#888888")
        tb.tag_configure("done", foreground="#3a7bd5")
        tb.tag_configure("warn", foreground="#e67e22")
        tb.tag_configure("err",  foreground="#c0392b")

    # ── Path loading (shared by buttons and drop handlers) ────────────────────

    def _load_unpack_path(self, file_path: str):
        self.log(f"Opened {file_path}", "info")
        filenames = generate_channel_filenames(Path(file_path))
        for channel in CHANNELS:
            self.unpack_path_inputs[channel].set(filenames[channel])
            self.log(f"Set {channel.upper()} channel output: {filenames[channel]}", "ok")
        self.unpack_path.set(file_path)

        try:
            with Image.open(file_path) as img:
                rgba = img.convert("RGBA")
                self.unpack_preview.configure(
                    image=self._make_preview(rgba), text="",
                )
                for channel, band in zip(CHANNELS, rgba.split()):
                    self.unpack_thumbs[channel].configure(
                        image=self._make_thumb(band), text="",
                    )
        except Exception as e:
            self.log(f"Preview error: {e}", "err")

    def _load_pack_path(self, channel: str, file_path: str):
        self.pack_path_inputs[channel].set(file_path)
        self.log(f"Set {channel.upper()} channel path: {file_path}", "ok")

        try:
            with Image.open(file_path) as img:
                self.pack_thumbs[channel].configure(
                    image=self._make_thumb(img), text="",
                )
        except Exception as e:
            self.log(f"Preview error: {e}", "err")

        self._update_pack_preview()

    def _update_pack_preview(self):
        """Composite all currently-loaded pack channels into a live preview."""
        bands = {}
        size = None

        for channel in CHANNELS:
            path = self.pack_path_inputs[channel].get()
            if not path:
                continue
            try:
                with Image.open(path) as img:
                    band = img.convert("L")
                    band.load()
                    bands[channel] = band.copy()
                    if size is None:
                        size = band.size
            except Exception:
                pass

        if not bands:
            self.pack_preview.configure(image=None, text="No image loaded")
            return

        black = Image.new("L", size, 0)
        alpha = Image.new("L", size, 255)

        try:
            composite = Image.merge("RGBA", (
                bands.get("r", black),
                bands.get("g", black),
                bands.get("b", black),
                bands.get("a", alpha),
            ))
            self.pack_preview.configure(
                image=self._make_preview(composite), text="",
            )
        except Exception as e:
            self.log(f"Preview error: {e}", "err")

    # ── Actions ───────────────────────────────────────────────────────────────

    def select_unpack_path(self):
        file_path = filedialog.askopenfilename(
            title="Select a file to unpack", filetypes=[("PNG files", "*.png")]
        )
        if not file_path:
            self.log("No file selected.", "info")
            return
        self._load_unpack_path(file_path)

    def select_pack_path(self, channel):
        file_path = filedialog.askopenfilename(
            title=f"Select {channel.upper()} channel file", filetypes=[("PNG files", "*.png")]
        )
        if not file_path:
            self.log("No file selected for packing", "info")
            return
        self._load_pack_path(channel, file_path)

    def unpack_channels(self):
        file_path = self.unpack_path.get()
        if not file_path:
            self.log("Please select an image to unpack", "warn")
            return

        save_dir = filedialog.askdirectory(
            title="Select output directory",
            initialdir=Path.cwd(),
        )
        if not save_dir:
            self.log("No output directory selected", "info")
            return

        try:
            with Image.open(file_path) as img:
                img = img.convert("RGBA")
                channels = dict(zip(CHANNELS, img.split()))
        except Exception as e:
            self.log(f"Failed to open image: {e}", "err")
            return

        save_dir = Path(save_dir)
        filenames = generate_channel_filenames(Path(file_path))
        for channel, img_obj in channels.items():
            output_file = save_dir / filenames[channel]
            img_obj.save(output_file)
            self.unpack_path_inputs[channel].set(str(output_file))
            with Image.open(output_file) as saved:
                self.unpack_thumbs[channel].configure(
                    image=self._make_thumb(saved), text="",
                )
            self.log(f"Saved {channel.upper()} channel: {output_file}", "ok")

        self.log("Unpacking complete!", "done")

    def pack_channels(self):
        files = [self.pack_path_inputs[c].get() for c in CHANNELS]
        if not all(files):
            self.log("Please select all 4 channel files before packing", "warn")
            return

        save_dir = filedialog.askdirectory(
            title="Select output directory",
            initialdir=Path.cwd(),
        )
        if not save_dir:
            self.log("No output directory selected", "info")
            return

        try:
            channels = []
            for f in files:
                with Image.open(f) as img:
                    channels.append(img.convert("L"))

            sizes = [img.size for img in channels]
            if len(set(sizes)) != 1:
                self.log("All channel images must be the same dimensions", "err")
                return

            r_stem = Path(files[0]).stem
            out_stem = r_stem[:-2] if r_stem.endswith("_r") else r_stem
            output_file = Path(save_dir) / f"{out_stem}_rgba.png"

            merged = Image.merge("RGBA", channels)
            merged.save(output_file)

            self.pack_preview.configure(
                image=self._make_preview(merged), text="",
            )
            self.log(f"Packed channels into {output_file}!", "done")
        except Exception as e:
            self.log(f"Failed to pack channels: {e}", "err")

    def log(self, message, tag="info"):
        tb = self.log_textbox._textbox
        tb.configure(state="normal")
        tb.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] ", "time")
        tb.insert(tk.END, message + "\n", tag)
        tb.see(tk.END)
        tb.configure(state="disabled")


def generate_channel_filenames(path: Path):
    return {c: f"{path.stem}_{c}{path.suffix}" for c in CHANNELS}
