if not hasattr(self, '_gui_initialized'):
    try:
        import tkinter as tk
        from tkinter import ttk
        self._initialize_gui()
        self._gui_initialized = True
    except Exception as e:
        print(f'[ERROR] GUI init failed: {e}')
        return False