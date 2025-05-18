import os
import tkinter as tk
from tkinter import messagebox
import random

"""
A visual role selection system using a GUI. 

Step 1 Allows the user to select the number of players (1–6); 

Step 2 Collects player names; 

Step 3 Presents each player with 3 randomly assigned role cards. Players can click on any card to select their desired role, 
and the selected card will be highlighted in green. 

Step 4 After all players have selected their roles, click the "Finish Selection" button in the top-right corner to proceed.

Step 5 In the final selection screen, clicking "re-randomize" will return to the role cards selection interface, 
removing previously chosen role cards from the pool and allowing players to start a new round of selection. 
If "GG" (I'm done) is clicked instead, the entire selection system will be closed.

！！！Due to UI layout and card content length, each skill description is limited to 40 characters. If the full description 
is not visible, hover over the skill box to view the full text. ！！！

Upcoming updates：
-Selection result UI update
-Return to the previous window while retaining the character culling pool？
"""

# Setup window
class PlayerSetupGUI:
    def __init__(self, master, wizard_dict):
        self.master = master
        self.master.title("玩家设置")
        self.wizard_dict = wizard_dict
        self.font_main = ("Microsoft YaHei", 11)
        self.master.geometry("600x300")
        self.player_entries = []
        self.num_players = 0

        self.build_step1()

    def build_step1(self):
        self.clear_window()

        tk.Label(self.master, text="请选择玩家人数（最多六名）：", font=("Microsoft YaHei", self.font_main[1]+1, "bold"), fg="red").pack(pady=20,anchor='center')

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
        # Initial size of the window
        self.master.geometry("1500x800")
        # Selects icon for tkinter
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),  'doc', 'icon.ico'))
        self.master.iconbitmap(icon_path)
        self.player_names = player_names
        self.wizard_dict = wizard_dict
        self.n_select = n_select
        self.selected_wizards = {name: None for name in player_names}
        self.game_used = set()
        self.wizard_options = {}
        self.card_frames = {}
        self.available_wizards = list(wizard_dict.items())
        random.shuffle(self.available_wizards)
        self.font_main = ("Microsoft YaHei", 15)    
        
        self.screen_w = self.master.winfo_screenwidth()
        self.screen_h = self.master.winfo_screenheight()
        
        
        self.build_scrollable_ui()

    # def build_scrollable_ui(self):
    #     self.canvas = tk.Canvas(self.master, borderwidth=0)
    #     self.scroll_frame = tk.Frame(self.canvas)
    #     self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
    #     self.canvas.configure(yscrollcommand=self.scrollbar.set)

    #     self.scrollbar.pack(side="right", fill="y")
    #     self.canvas.pack(side="left", fill="both", expand=True)
    #     self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

    #     self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    #     self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    #     self.build_cards(self.scroll_frame)

    #     self.finish_btn = tk.Button(self.master, text="完成选择", command=self.finish_selection)
    #     self.finish_btn.pack(pady=10)

    def build_scrollable_ui(self):
        
        # Wrapper frame for layout (canvas + button)
        wrapper = tk.Frame(self.master)
        wrapper.pack(fill="both", expand=True)
        
        # Pack finish button *outside* the scrollable wrapper
        self.finish_btn = tk.Button(self.master, text="完成选择", command=self.finish_selection)
        self.finish_btn.pack(pady=10) 

        # Canvas and scrollbar
        self.canvas = tk.Canvas(wrapper, borderwidth=0)
        self.scrollbar = tk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollable frame inside canvas
        self.scroll_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Update scrollregion when contents change
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Scroll with mouse wheel
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # Build content in scrollable frame
        self.build_cards(self.scroll_frame)

    def build_cards(self, container):
        
        # screen_w = self.master.winfo_screenwidth()
        # screen_h = self.master.winfo_screenheight()
        # print(screen_w, screen_h)
        card_width = (self.screen_w-56) / 6
        card_height = (self.screen_h-140) / 3  # in pixels
        
        wrap_max = card_width - 10
        max_text_length = 10000

        # Maximum number of rows - fit UI
        max_rows = 3
        used_wizards_now = set()
        for i, player in enumerate(self.player_names):
            row = i % max_rows
            col = i // max_rows
            player_frame = tk.Frame(container, relief=tk.FLAT, borderwidth=1)
            player_frame.grid(row=row, column=col, padx=3, pady=1, sticky='n')
            label = tk.Label(player_frame, text=f"{player}，请选择你的职业：", font=("Microsoft YaHei", self.font_main[1], "bold"), fg="red")
            label.pack(anchor="w")
            card_row = tk.Frame(player_frame)
            card_row.pack()

            # print(len(self.available_wizards), len(used_wizards_now))
            options = []
            while len(options) < self.n_select and self.available_wizards:
                wiz = self.available_wizards.pop()
                if wiz[0] not in used_wizards_now:
                    options.append(wiz)
                    used_wizards_now.add(wiz[0])

            self.wizard_options[player] = options
            self.card_frames[player] = []

            for wiz_name, skills in options:
                
                # =====================================
                # flexible card size
                # f = tk.Frame(card_row, relief=tk.RIDGE, borderwidth=2, bg="white")

                # =====================================
                # determined card size
                f = tk.Frame(card_row, relief=tk.RIDGE, borderwidth=2, bg="white", 
                             width=card_width, height=card_height)
                f.pack_propagate(False)  # Prevent resizing to fit contents
                
                # ==========================================================
                f.pack(side="left", padx=2, pady=2)
                f.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                name_label = tk.Label(f, text=wiz_name, font=("Microsoft YaHei", self.font_main[1], "bold"), fg="blue", bg="white")
                name_label.pack(pady=0)
                name_label.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                for skill, desc in skills.items():
                    skill_label = tk.Label(f, text=skill, font=("Microsoft YaHei", self.font_main[1]-1, "bold"), fg="darkblue", bg="white", anchor="w", justify="left")
                    skill_label.pack(anchor="w", padx=2, pady=0)
                    skill_label.bind("<Button-1>", lambda e, p=player, w=wiz_name: self.select_wizard(p, w))

                    desc_label = tk.Label(f, text=desc[:max_text_length] + ('...' if len(desc) > max_text_length else ''), 
                                          font=self.font_main, wraplength=wrap_max, justify="left", bg="white")
                    desc_label.pack(anchor="w", padx=2)
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

    def clear_main_ui(self):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        if hasattr(self, 'scrollbar'):
            self.scrollbar.destroy()
        if hasattr(self, 'finish_btn'):
            self.finish_btn.destroy()
        for widget in self.master.winfo_children():
            widget.destroy()

    def restart_selection(self, summary_window):
        summary_window.destroy()
        
        # Removed played roles 
        used = set(self.selected_wizards.values())
        self.game_used.update(used)
        print(self.game_used)
        
        # print(len(self.available_wizards))
        self.available_wizards = [(k, v) for k, v in self.wizard_dict.items() if k not in self.game_used]
        print(len(self.available_wizards))
        
        # Check if enough is allocated
        total_needed = len(self.player_names) * self.n_select
        if len(self.available_wizards) < total_needed:
            messagebox.showwarning("卡池不足", "剩余角色不足以分配给所有玩家，将重新洗牌。")
            self.available_wizards = self.wizard_dict
            # return
        
        random.shuffle(self.available_wizards)
        # Rebuild role selector UI
        self.selected_wizards = {name: None for name in self.player_names}
        self.wizard_options.clear()
        self.card_frames.clear()

        self.clear_main_ui()
        self.build_scrollable_ui()

    def show_summary_window(self):
        summary = tk.Toplevel(self.master)
        summary.title("最终选择展示")
        summary.geometry("%ix%i"%(self.screen_w, self.screen_h))

        for i, player in enumerate(self.player_names):
            tk.Label(summary, text=f"{player} 选择了 {self.selected_wizards[player]}", 
                     font=("Microsoft YaHei", self.font_main[1]+10, "bold"), fg="blue").pack(anchor="w", padx=20,pady=10)
            for skill, desc in self.wizard_dict[self.selected_wizards[player]].items():
                tk.Label(summary, text=f"  {skill}: {desc}", 
                         wraplength=self.screen_w-50, justify="left", 
                         font=("Microsoft YaHei", self.font_main[1]+7, "bold")).pack(anchor="w", padx=20)

        btn_frame = tk.Frame(summary)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="重新随机", font=self.font_main,
                  command=lambda: self.restart_selection(summary)).pack(padx=10)
        tk.Button(btn_frame, text="不想玩辣", font=self.font_main, command=self.master.quit).pack(padx=10)

if __name__ == '__main__':
    from src.wizards import load_wizards
    wizard_dict = load_wizards()
    root = tk.Tk()
    app = PlayerSetupGUI(root, wizard_dict)
    root.mainloop()

