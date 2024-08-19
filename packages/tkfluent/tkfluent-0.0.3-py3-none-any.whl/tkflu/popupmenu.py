from tkinter import Toplevel
from .frame import FluFrame


class FluPopupMenuWindow(Toplevel):
    def __init__(self, *args, transparent_color="#ffefa2", mode="light", width=100, height=46, **kwargs):
        super().__init__(*args, background=transparent_color, **kwargs)

        self.theme(mode=mode)

        self.geometry(f"{width}x{height}")

        self.transient_color = transparent_color
        self.overrideredirect(True)
        self.attributes("-transparentcolor", transparent_color)

        self.withdraw()

        self.bind("<FocusOut>", self._event_focusout)

    def _event_focusout(self, event=None):
        self.withdraw()

    def popup(self, x, y):
        self.geometry(f"+{x}+{y}")

    def theme(self, mode=None):
        if mode:
            self.mode = mode
        for widget in self.winfo_children():
            if hasattr(widget, "theme"):
                widget.theme(mode=self.mode.lower())


class FluPopupMenu(FluFrame):
    def __init__(self, *args, width=100, height=46, transparent_color="#ffefa2", style="popupmenu", **kwargs):
        self.window = FluPopupMenuWindow(transparent_color=transparent_color, width=width, height=height)

        super().__init__(self.window, *args, style=style, **kwargs)

        self.pack(fill="both", expand="yes", padx=5, pady=5)

    def wm_attributes(self, *args, **kwargs):
        self.window.wm_attributes(*args, **kwargs)

    attributes = wm_attributes

    def wm_protocol(self, *args,  **kwargs):
        self.window.wm_protocol(*args, **kwargs)

    protocol = wm_protocol

    def wm_deiconify(self, *args,  **kwargs):
        self.window.wm_deiconify(*args, **kwargs)

    deiconify = wm_deiconify

    def wm_withdraw(self, *args,  **kwargs):
        self.window.wm_withdraw(*args, **kwargs)

    withdraw = wm_withdraw

    def wm_iconify(self, *args,  **kwargs):
        self.window.wm_iconify(*args, **kwargs)

    iconify = wm_iconify

    def wm_resizable(self, *args,  **kwargs):
        self.window.wm_resizable(*args, **kwargs)

    resizable = wm_resizable

    def wm_geometry(self, *args,  **kwargs):
        self.window.wm_geometry(*args, **kwargs)

    geometry = wm_geometry

    def wm_popup(self, x, y):
        self.window.popup(x=x, y=y)

    popup = wm_popup
