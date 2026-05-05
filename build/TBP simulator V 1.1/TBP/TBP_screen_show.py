# THREE BODY PROBLEM!!

# =========
#   UNITS
# =========
# mass → kg
# position → m (미터)
# velocity → m/s
# acceleration → m/s²
# datatime → s (초)
# G → 6.674e-11 (N·m²/kg²)

import sys
import numpy as np
import TBP_calculate
from TBP_data_load import TBPjson
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Planet:
	def __init__(self, mass, position, velocity, acceleration):
		# mass: 질량
		# position: 좌표 (x,y)
		# velocity: velocity, 속도 (vx, vy)
		# accelation: accelation, 가속도 (ax, ay)
		# 위에 친구들은 벡터입니다. np.array를 통해 지정했어요.
		# 왜 행렬로 굳이 지정했냐고요? 처음에 그냥하려 했는데 행렬 합으로 계산 및 코드가 더 깔끔해집니다.
		self.pos = np.array(position)
		self.vel = np.array(velocity)
		self.acc = np.array(acceleration)
		self.mass = mass

	def get_planet_data(self):
		# 값 주는 함수입니다.
		return self.mass, self.pos, self.vel, self.acc

	def move(self, dt):
		self.pos += self.vel * dt

	def accelation(self, dt):
		self.vel += self.acc * dt

	def set_accelation(self, value):
		self.acc = np.array(value)

	def add_accelation(self, value):
		self.acc += np.array(value)


"""
masses = np.array([1e30, 1e30, 1e30])

positions = np.array([
	[-1.0e11, 0.0],
	[1.0e11, 0.0],
	[0.0, 0.0]
])

velocities = np.array([
	[1.2e4, 1.6e4],
	[1.2e4, 1.6e4],
	[-2.4e4, -3.2e4]
])
"""

if len(sys.argv) > 1:
	json_path = sys.argv[1]
	R = TBPjson(json_path)
	p1_data, p2_data, p3_data = R.get_value()
	sc = R.file_data.get('simconfig', {})

	print(sc)

	p1 = Planet(mass=p1_data['mass'], position=p1_data['position'], velocity=p1_data['velocity'],
	            acceleration=[0.0, 0.0])
	p2 = Planet(mass=p2_data['mass'], position=p2_data['position'], velocity=p2_data['velocity'],
	            acceleration=[0.0, 0.0])
	p3 = Planet(mass=p3_data['mass'], position=p3_data['position'], velocity=p3_data['velocity'],
	            acceleration=[0.0, 0.0])

	datatime = sc.get('dt', 3600)
	steps = int(sc.get('steps', 5000))
	interval = int(sc.get('interval', 10))
	trail_len = int(sc.get('trail_len', 300))
	print(sc)
	xlim = float(sc.get('xlim', 3e11))
	history = []

	for step in range(steps):
		# 가속도 초기화 후 계산
		p1.set_accelation([0.0, 0.0])
		p1.add_accelation(TBP_calculate.TBPCalculate(p1, p2).calculate_gravity())
		p1.add_accelation(TBP_calculate.TBPCalculate(p1, p3).calculate_gravity())

		p2.set_accelation([0.0, 0.0])
		p2.add_accelation(TBP_calculate.TBPCalculate(p2, p1).calculate_gravity())
		p2.add_accelation(TBP_calculate.TBPCalculate(p2, p3).calculate_gravity())

		p3.set_accelation([0.0, 0.0])
		p3.add_accelation(TBP_calculate.TBPCalculate(p3, p1).calculate_gravity())
		p3.add_accelation(TBP_calculate.TBPCalculate(p3, p2).calculate_gravity())

		# 속도, 위치 업데이트
		for p in [p1, p2, p3]:
			p.accelation(datatime)
			p.move(datatime)

		# 위치 저장
		history.append([p1.pos.copy(), p2.pos.copy(), p3.pos.copy()])
	history = np.array(history)

	plt.rcParams['font.family'] = 'Malgun Gothic'
	plt.rcParams['axes.unicode_minus'] = False

	fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
	ax.set_facecolor('black')
	print(3e11)
	print(xlim)
	ax.set_xlim(-xlim, xlim)
	ax.set_ylim(-xlim, xlim)
	ax.set_title('Three Body Problem', color='white')

	time_text = ax.text(0.02, 0.97, '', transform=ax.transAxes, color='white', fontsize=10, va='top')

	colors = ['cyan', 'orange', 'lime']
	dots = [ax.plot([], [], 'o', color=c, markersize=8)[0] for c in colors]
	lines = [ax.plot([], [], '-', color=c, alpha=0.4, linewidth=0.8)[0] for c in colors]

	trail_len = int(sc.get('trail_len', 300))
	print(trail_len)



	def update(frame):
		if frame < 0:
			time_text.set_text(f'시작까지 {abs(frame)//1000+1}초...')
			for i in range(3):
				dots[i].set_data([], [])
				lines[i].set_data([], [])
			return dots + lines + [time_text]

		for i in range(3):
			dots[i].set_data([history[frame, i, 0]], [history[frame, i, 1]])
			start = max(0, frame - trail_len)
			lines[i].set_data(history[start:frame, i, 0], history[start:frame, i, 1])

		elapsed = frame * datatime
		days = int(elapsed // 86400)
		years = days // 365
		remaining_days = days % 365
		time_text.set_text(f'경과 시간: {years}년 {remaining_days}일')

		return dots + lines + [time_text]


	delay_frames = int(3000/interval)  # 3초 대기 (interval 단위)
	ani = animation.FuncAnimation(fig, update, frames=range(-delay_frames, steps, 2), interval=interval, blit=True)
	plt.tight_layout()
	plt.show()
