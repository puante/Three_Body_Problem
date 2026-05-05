"""
Project: 삼체 문제 시뮬레이션 프로그램 제작 및 이를 통한 카오스 이론 분석
마지막 수정일: 2026.05.05
현 버전: V 1.0
Copyright (c) 2026 PuantE
Licensed under the MIT License
"""


import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import json
import subprocess
import sys
import os
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

		tk.Label(root, text="[ 행성 초기값 ]", font=('맑은 고딕', 20)).pack(pady=(10, 2))

		for key, label in fields.items():
			frame = tk.Frame(root)
			frame.pack(fill='x', padx=20, pady=2)
			tk.Label(frame, text=label, width=10).pack(side='left')
			entry = tk.Entry(frame)
			entry.pack(side='right', expand=True, fill='x')
			self.entries[key] = entry

		tk.Label(root, text="[ 시뮬레이션 설정 ]", font=('맑은 고딕', 20)).pack(pady=(15, 2))

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

		tk.Button(root, text="시뮬레이션 실행", command=self.run_sim,
		          bg='green', fg='white', font=('맑은 고딕', 11, 'bold'), height=2).pack(pady=15, fill='x', padx=20)

	def _get_float(self, key):
		val = self.entries[key].get().strip()
		if val == '':
			raise ValueError(f"'{key}' 값이 비어있습니다.\n값을 제대로 입력하였는지 다시 한 번 확인하십시오.")
		return float(val)

	def _get_int(self, key):
		val = self.entries[key].get().strip()
		if val == '':
			raise ValueError(f"'{key}' 값이 비어있습니다.\n값을 제대로 입력하였는지 다시 한 번 확인하십시오.")
		return int(val)

	def _build_data(self):
		return {
			"planetdata": {
				f'p{i}': {
					'mass': self._get_float(f'p{i}_mass'),
					'position': [self._get_float(f'p{i}_x'), self._get_float(f'p{i}_y')],
					'velocity': [self._get_float(f'p{i}_vx'), self._get_float(f'p{i}_vy')]
				} for i in range(1, 4)
			},
			"simconfig": {
				"dt": self._get_float('dt'),
				"steps": self._get_int('steps'),
				"interval": self._get_int('interval'),
				"trail_len": self._get_int('trail_len'),
			}
		}

	def load_file(self):
		path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
		if not path:
			return
		try:
			with open(path, 'r', encoding='utf-8') as f:
				data = json.load(f)
		except FileNotFoundError:
			messagebox.showerror("오류", "파일을 찾을 수 없습니다.")
			return
		except json.JSONDecodeError:
			messagebox.showerror("오류", "JSON 형식이 잘못되었습니다.")
			return

		try:
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
		except KeyError as e:
			messagebox.showerror("오류", f"JSON 구조가 잘못되었습니다. {e} 키가 없는 것으로 보입니다.")
			return

		if 'simconfig' in data:
			sc = data['simconfig']
			for key in ['dt', 'steps', 'interval', 'trail_len']:
				if key in sc:
					self.entries[key].delete(0, tk.END)
					self.entries[key].insert(0, sc[key])

		self.file_path = path

	def save_file(self):
		try:
			data = self._build_data()
		except ValueError as e:
			messagebox.showerror("오류", str(e))
			return

		if not self.file_path:
			self.file_path = filedialog.asksaveasfilename(defaultextension=".json")
			if not self.file_path:
				return

		try:
			with open(self.file_path, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=4, ensure_ascii=False)
			messagebox.showinfo("저장 완료", "성공적으로 저장되었습니다.")
		except Exception as e:
			messagebox.showerror("오류", f"저장에 실패하였습니다. {e}")

	def run_sim(self):
		try:
			data = self._build_data()
		except ValueError as e:
			messagebox.showerror("오류", str(e))
			return

		try:
			tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
			json.dump(data, tmp, ensure_ascii=False)
			tmp.close()
			if getattr(sys, 'frozen', False):
				exe_dir = os.path.dirname(sys.executable)
				screen_exe = os.path.join(exe_dir, 'TBP/TBP_screen_show.exe')
				subprocess.Popen([screen_exe, tmp.name])
			else:
				subprocess.Popen([sys.executable, 'TBP/TBP_screen_show.py', tmp.name])
		except Exception as e:
			messagebox.showerror("오류", f"실행에 실패하였습니다. {e}")


if __name__ == "__main__":
	R = tk.Tk()
	R.iconbitmap("TBP/image/TBP_program_icon.ico")
	app = TBPGUI(R)
	R.mainloop()