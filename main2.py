import random
import tkinter as tk
import math

class Roulette:
    def __init__(self, root):
        self.root = root
        self.root.title("ルーレット")
        self.root.geometry("400x500")
        
        # ルーレットの項目の基本設定（初期値は空）
        self.base_items = []
        self.colors = ["red", "blue", "green", "yellow", "orange", "purple"]
        
        # 初期項目を追加するためのダイアログ表示
        self.setup_initial_items()
    
    def setup_initial_items(self):
        """初期項目を設定するダイアログ"""
        setup_window = tk.Toplevel(self.root)
        setup_window.title("初期項目設定")
        setup_window.geometry("300x400")
        setup_window.grab_set()  # モーダルウィンドウにする
        
        tk.Label(setup_window, text="ユーザー名を入力してください", font=("Arial", 12)).pack(pady=10)
        
        self.temp_items = []
        self.entry_widgets = []
        
        # 6個の入力欄を作成
        for i in range(6):
            frame = tk.Frame(setup_window)
            frame.pack(pady=5, padx=20, fill=tk.X)
            
            tk.Label(frame, text=f"項目{i+1}:", width=6).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=20)
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.entry_widgets.append(entry)
        
        # ボタンフレーム
        button_frame = tk.Frame(setup_window)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="確定", command=lambda: self.apply_initial_items(setup_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="デフォルト使用", command=lambda: self.use_default_items(setup_window)).pack(side=tk.LEFT, padx=5)
    
    def apply_initial_items(self, window):
        """入力された項目を適用"""
        for entry in self.entry_widgets:
            item = entry.get().strip()
            if item:
                self.base_items.append(item)
        
        if not self.base_items:
            # 何も入力されていない場合はデフォルトを使用
            self.use_default_items(window)
            return
        
        window.destroy()
        self.initialize_roulette()
    
    def use_default_items(self, window):
        """デフォルトユーザー名を使用"""
        self.base_items = ["ユーザー1", "ユーザー2", "ユーザー3", "ユーザー4", "ユーザー5", "ユーザー6"]
        window.destroy()
        self.initialize_roulette()
    
    def initialize_roulette(self):
        
        # 現在表示する項目数（デフォルトは4個）
        self.num_items = 4
        self.items = self.base_items[:self.num_items]
        
        # 項目数調整用スライダー
        self.slider_frame = tk.Frame(root)
        self.slider_frame.pack(pady=10)
        
        tk.Label(self.slider_frame, text="ユーザー数:").pack(side=tk.LEFT)
        self.items_slider = tk.Scale(self.slider_frame, from_=3, to=6, orient=tk.HORIZONTAL, 
                       command=self.update_items_count, length=200)
        self.items_slider.set(4)
        self.items_slider.pack(side=tk.LEFT, padx=10)
        # アニメーション用変数
        self.rotation_angle = 0
        self.is_spinning = False
        
        # キャンバスの作成
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack(pady=20)
        
        # 結果表示ラベル
        self.result_label = tk.Label(self.root, text="結果: まだ回していません", font=("Arial", 14))
        self.result_label.pack(pady=10)
        
        # ボタン
        self.spin_button = tk.Button(self.root, text="ルーレットを回す", command=self.spin, 
                                   font=("Arial", 12), bg="lightblue")
        self.spin_button.pack(pady=10)
        
        # 項目編集用
        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(pady=20)
        
        tk.Label(self.edit_frame, text="項目を編集:").pack()
        self.item_entry = tk.Entry(self.edit_frame, width=20)
        self.item_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.edit_frame, text="追加", command=self.add_item).pack(side=tk.LEFT, padx=5)
        tk.Button(self.edit_frame, text="削除", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        
        # 初期描画
        self.draw_roulette()
    
    def update_items_count(self, value):
        """項目数を更新"""
        self.num_items = int(value)
        self.items = self.base_items[:self.num_items]
        self.draw_roulette()
    
    def draw_roulette(self):
        self.canvas.delete("all")
        if not self.items:
            return
            
        center_x, center_y = 150, 150
        radius = 120
        
        # 各項目の角度
        angle_per_item = 360 / len(self.items)
        
        for i, item in enumerate(self.items):
            start_angle = i * angle_per_item + self.rotation_angle
            color = self.colors[i % len(self.colors)]
            
            # 扇形を描画
            self.canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle_per_item,
                fill=color, outline="black", width=2
            )
            
            # テキストを描画
            text_angle = math.radians(start_angle + angle_per_item / 2)
            text_x = center_x + (radius * 0.7) * math.cos(-text_angle)
            text_y = center_y + (radius * 0.7) * math.sin(-text_angle)
            
            self.canvas.create_text(text_x, text_y, text=item, font=("Arial", 10), fill="black")
        
        # 中心点
        self.canvas.create_oval(center_x-5, center_y-5, center_x+5, center_y+5, fill="black")
        
        # ポインター（固定位置）
        self.canvas.create_polygon(center_x, center_y-radius-10, 
                                 center_x-10, center_y-radius+10,
                                 center_x+10, center_y-radius+10,
                                 fill="red", outline="black")
    
    def spin(self):
        if not self.items or self.is_spinning:
            return
            
        self.is_spinning = True
        self.spin_button.config(state="disabled")
        self.result_label.config(text="回転中...")
        
        # 回転回数とスピード設定
        self.spin_speed = 20
        self.spin_duration = 0
        self.max_duration = 100  # 約2秒
        
        self.animate_spin()
    
    def animate_spin(self):
        if self.spin_duration < self.max_duration:
            # 徐々に減速
            deceleration = max(1, self.spin_speed * (self.max_duration - self.spin_duration) / self.max_duration)
            self.rotation_angle = (self.rotation_angle + deceleration) % 360
            
            self.draw_roulette()
            self.spin_duration += 1
            
            # 次のフレームをスケジュール
            self.root.after(50, self.animate_spin)
        else:
            # 回転終了
            self.finish_spin()
    
    def finish_spin(self):
        self.is_spinning = False
        self.spin_button.config(state="normal")
        
        # 結果を計算（ポインターの位置から逆算）
        angle_per_item = 360 / len(self.items)
        # ポインターは上向きなので、90度の位置にある項目を選択
        pointer_angle = (90 - self.rotation_angle) % 360
        selected_index = int(pointer_angle // angle_per_item)
        
        selected_item = self.items[selected_index]
        self.result_label.config(text=f"結果: {selected_item}")
    
    def add_item(self):
        new_item = self.item_entry.get().strip()
        if new_item and new_item not in self.items:
            self.items.append(new_item)
            self.item_entry.delete(0, tk.END)
            self.draw_roulette()
    
    def remove_item(self):
        item_to_remove = self.item_entry.get().strip()
        if item_to_remove in self.items:
            self.items.remove(item_to_remove)
            self.item_entry.delete(0, tk.END)
            self.draw_roulette()

if __name__ == "__main__":
    root = tk.Tk()
    app = Roulette(root)
    root.mainloop()