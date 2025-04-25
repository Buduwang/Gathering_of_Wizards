import os
import tkinter as tk
from tkinter import messagebox
import random

"""
A visual role selection system using a GUI. 
Step 1 allows the user to select the number of players (1–6); 
Step 2 collects player names; 
Step 3 presents each player with 3 randomly assigned role cards. Players can click on any card to select their desired 
role, and the selected card will be highlighted in green. Due to UI layout and card content length, each skill 
description is limited to 40 characters. If the full description is not visible, hover over the skill box to view 
the full text. After all players have selected their roles, click the "Finish Selection" button in the top-right corner to proceed.
"""

# Setup window
class PlayerSetupGUI:
    def __init__(self, master, wizard_dict):
        self.master = master
        self.master.title("玩家设置")
        self.wizard_dict = wizard_dict
        self.font_main = ("Microsoft YaHei", 11)
        self.master.geometry("400x300")
        self.player_entries = []
        self.num_players = 0

        self.build_step1()

    def build_step1(self):
        self.clear_window()

        tk.Label(self.master, text="请选择玩家人数（最多六名）：", font=("Microsoft YaHei", 12, "bold"), fg="red").pack(pady=20,anchor='center')

        btn_frame = tk.Frame(self.master)
        btn_frame.pack()
        # Maximum 6 players
        for i in range(1, 7):
            b = tk.Button(btn_frame, text=str(i), width=4, font=self.font_main,
                          command=lambda n=i: self.build_step2(n))
            b.pack(side="left", padx=5, pady=50)

    def build_step2(self, num):
        self.clear_window()
        self.num_players = num

        tk.Label(self.master, text="请输入每位玩家的昵称：", font=self.font_main).pack(pady=10)

        self.player_entries = []
        for i in range(num):
            entry = tk.Entry(self.master, font=self.font_main)
            entry.pack(pady=2)
            entry.insert(0, f"玩家{i+1}")
            self.player_entries.append(entry)

        tk.Button(self.master, text="开始选择职业", command=self.launch_wizard_selector).pack(pady=10)

    def launch_wizard_selector(self):
        player_names = [entry.get().strip() or f"玩家{i+1}" for i, entry in enumerate(self.player_entries)]
        self.master.destroy()

        root = tk.Tk()
        app = WizardSelectorGUI(root, player_names, self.wizard_dict, n_select=3)
        root.mainloop()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Character selector
class WizardSelectorGUI:
    def __init__(self, master, player_names, wizard_dict, n_select=3):
        self.master = master
        self.master.title("职业选择")
        self.master.geometry("1500x800")

        # use icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),  'doc', 'icon.ico'))
        self.master.iconbitmap(icon_path)

        self.player_names = player_names
        self.wizard_dict = wizard_dict
        self.n_select = n_select
        self.selected_wizards = {name: None for name in player_names}
        self.wizard_options = {}
        self.card_frames = {}

        self.available_wizards = list(wizard_dict.items())
        random.shuffle(self.available_wizards)

        self.font_main = ("Microsoft YaHei", 11)

        self.build_scrollable_ui()



    def build_scrollable_ui(self):
        self.canvas = tk.Canvas(self.master, borderwidth=0)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.build_cards(self.scroll_frame)

        self.finish_btn = tk.Button(self.master, text="完成选择", command=self.finish_selection)
        self.finish_btn.pack(pady=10)


    def build_cards(self, container):
        # Maximum number of rows - fit UI
        max_rows = 3
        used_wizards = set()

        for i, player in enumerate(self.player_names):
            row = i % max_rows
            col = i // max_rows

            player_frame = tk.Frame(container, relief=tk.FLAT, borderwidth=1)
            player_frame.grid(row=row, column=col, padx=10, pady=10, sticky='n')

            label = tk.Label(player_frame, text=f"{player}，请选择你的职业：", font=("Microsoft YaHei", 11, "bold"), fg="red")
            label.pack(anchor="w")

            card_row = tk.Frame(player_frame)
            card_row.pack()

            options = []
            while len(options) < self.n_select and self.available_wizards:
                wiz = self.available_wizards.pop()
                if wiz[0] not in used_wizards:
                    options.append(wiz)
                    used_wizards.add(wiz[0])

            self.wizard_options[player] = options
            self.card_frames[player] = []

            for wiz_name, skills in options:
                f = tk.Frame(card_row, relief=tk.RIDGE, borderwidth=2, bg="white")
                f.pack(side="left", padx=5, pady=5)
                f.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                name_label = tk.Label(f, text=wiz_name, font=("Microsoft YaHei", 11, "bold"), fg="blue", bg="white")
                name_label.pack(pady=2)
                name_label.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                for skill, desc in skills.items():
                    skill_label = tk.Label(f, text=skill, font=("Microsoft YaHei", 10, "bold"), fg="darkblue", bg="white", anchor="w", justify="left")
                    skill_label.pack(anchor="w", padx=5)
                    skill_label.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                    desc_label = tk.Label(f, text=desc[:40] + ('...' if len(desc) > 40 else ''), font=self.font_main, wraplength=180, justify="left", bg="white")
                    desc_label.pack(anchor="w", padx=10)
                    desc_label.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))
                    desc_label.bind("<Enter>", lambda e, full=desc: self.show_tooltip(e.widget, full))
                    desc_label.bind("<Leave>", lambda e: self.hide_tooltip())

                self.card_frames[player].append((wiz_name, f))


    def show_tooltip(self, widget, text):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 20
        y += widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip, text=text, justify='left', background='lightyellow', relief='solid', borderwidth=1, wraplength=300, font=self.font_main)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def select_wizard(self, player, wizard):
        self.selected_wizards[player] = wizard
        for wiz_name, frame in self.card_frames[player]:
            color = "lightgreen" if wiz_name == wizard else "white"
            frame.config(bg=color)
            for widget in frame.winfo_children():
                widget.config(bg=color)

    def finish_selection(self):
        if None in self.selected_wizards.values():
            messagebox.showwarning("未完成", "请确保所有玩家都完成了职业选择！")
            return
        self.show_summary_window()

    def show_summary_window(self):
        summary = tk.Toplevel(self.master)
        summary.title("最终选择展示")
        summary.geometry("700x700")

        for i, player in enumerate(self.player_names):
            tk.Label(summary, text=f"{player} 选择了 {self.selected_wizards[player]}", font=("Microsoft YaHei", 12, "bold"), fg="blue").pack(anchor="w", pady=5)
            for skill, desc in self.wizard_dict[self.selected_wizards[player]].items():
                tk.Label(summary, text=f"  {skill}: {desc}", wraplength=650, justify="left", font=self.font_main).pack(anchor="w", padx=20)

        tk.Button(summary, text="GG", command=summary.destroy).pack(pady=10)




if __name__ == '__main__':
    from src.wizards import load_wizards
    wizard_dict = load_wizards()
    root = tk.Tk()
    app = PlayerSetupGUI(root, wizard_dict)
    root.mainloop()

