import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import json
import subprocess
import sys
import tempfile


class TBPGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("Three Body Problem")
		self.root.geometry("450x650")
		self.file_path = None
		self.entries = {}

		# 메뉴바
		menubar = Menu(root)
		file_menu = Menu(menubar, tearoff=0)
		file_menu.add_command(label="로드", command=self.load_file)
		file_menu.add_command(label="저장", command=self.save_file)
		menubar.add_cascade(label="파일", menu=file_menu)
		root.config(menu=menubar)

		# 행성 입력 필드
		fields = {
			"p1_mass": "P1 질량", "p1_x": "P1 x", "p1_y": "P1 y",
			"p1_vx": "P1 vx", "p1_vy": "P1 vy",
			"p2_mass": "P2 질량", "p2_x": "P2 x", "p2_y": "P2 y",
			"p2_vx": "P2 vx", "p2_vy": "P2 vy",
			"p3_mass": "P3 질량", "p3_x": "P3 x", "p3_y": "P3 y",
			"p3_vx": "P3 vx", "p3_vy": "P3 vy",
		}

		tk.Label(root, text="[ 행성 초기값 ]", font=('Arial', 10, 'bold')).pack(pady=(10, 2))

		for key, label in fields.items():
			frame = tk.Frame(root)
			frame.pack(fill='x', padx=20, pady=2)
			tk.Label(frame, text=label, width=10).pack(side='left')
			entry = tk.Entry(frame)
			entry.pack(side='right', expand=True, fill='x')
			self.entries[key] = entry

		# 추가 설정
		tk.Label(root, text="[ 시뮬레이션 설정 ]", font=('Arial', 10, 'bold')).pack(pady=(15, 2))

		sim_fields = {
			"dt": ("dt (초)", "3600"),
			"steps": ("총 프레임 수", "5000"),
			"interval": ("애니메이션 속도 (ms)", "10"),
			"trail_len": ("궤적 길이", "300"),
		}

		for key, (label, default) in sim_fields.items():
			frame = tk.Frame(root)
			frame.pack(fill='x', padx=20, pady=2)
			tk.Label(frame, text=label, width=18).pack(side='left')
			entry = tk.Entry(frame)
			entry.insert(0, default)
			entry.pack(side='right', expand=True, fill='x')
			self.entries[key] = entry

		# 실행 버튼
		tk.Button(root, text="시뮬레이션 실행", command=self.run_sim,
		          bg='green', fg='white', font=('Arial', 11, 'bold'), height=2).pack(pady=15, fill='x', padx=20)

	def load_file(self):
		path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
		if not path:
			return
		self.file_path = path
		with open(path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		pd = data['planetdata']
		for i in range(1, 4):
			p = f'p{i}'
			self.entries[f'{p}_mass'].delete(0, tk.END)
			self.entries[f'{p}_mass'].insert(0, pd[p]['mass'])
			self.entries[f'{p}_x'].delete(0, tk.END)
			self.entries[f'{p}_x'].insert(0, pd[p]['position'][0])
			self.entries[f'{p}_y'].delete(0, tk.END)
			self.entries[f'{p}_y'].insert(0, pd[p]['position'][1])
			self.entries[f'{p}_vx'].delete(0, tk.END)
			self.entries[f'{p}_vx'].insert(0, pd[p]['velocity'][0])
			self.entries[f'{p}_vy'].delete(0, tk.END)
			self.entries[f'{p}_vy'].insert(0, pd[p]['velocity'][1])

		# 시뮬레이션 설정도 json에 있으면 로드
		if 'simconfig' in data:
			sc = data['simconfig']
			for key in ['dt', 'steps', 'interval', 'trail_len']:
				if key in sc:
					self.entries[key].delete(0, tk.END)
					self.entries[key].insert(0, sc[key])

	def save_file(self):
		if not self.file_path:
			self.file_path = filedialog.asksaveasfilename(defaultextension=".json")
		data = {
			"_coment1": "삼체 시뮬레이션 값",
			"planetdata": {
				f'p{i}': {
					'mass': float(self.entries[f'p{i}_mass'].get()),
					'position': [float(self.entries[f'p{i}_x'].get()), float(self.entries[f'p{i}_y'].get())],
					'velocity': [float(self.entries[f'p{i}_vx'].get()), float(self.entries[f'p{i}_vy'].get())]
				} for i in range(1, 4)
			},
			"simconfig": {
				"dt": float(self.entries['dt'].get()),
				"steps": int(self.entries['steps'].get()),
				"interval": int(self.entries['interval'].get()),
				"trail_len": int(self.entries['trail_len'].get()),
			}
		}
		with open(self.file_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=4, ensure_ascii=False)
		messagebox.showinfo("저장 완료", "저장됐어!")

	def run_sim(self):
		data = {
			"planetdata": {
				f'p{i}': {
					'mass': float(self.entries[f'p{i}_mass'].get()),
					'position': [float(self.entries[f'p{i}_x'].get()), float(self.entries[f'p{i}_y'].get())],
					'velocity': [float(self.entries[f'p{i}_vx'].get()), float(self.entries[f'p{i}_vy'].get())]
				} for i in range(1, 4)
			},
			"simconfig": {
				"dt": float(self.entries['dt'].get()),
				"steps": int(self.entries['steps'].get()),
				"interval": int(self.entries['interval'].get()),
				"trail_len": int(self.entries['trail_len'].get()),
			}
		}

		# 임시 파일로 저장해서 넘기기
		tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
		json.dump(data, tmp, ensure_ascii=False)
		tmp.close()

		subprocess.Popen([sys.executable, "TBP_screen_show.py", tmp.name])


if __name__ == "__main__":
	R = tk.Tk()
	app = TBPGUI(R)
	R.mainloop()
