import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 상수
G = 6.674e-11  # 중력상수

# 초기 설정 (질량, 위치, 속도)
# 8자 궤도 (안정적인 삼체 해)
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

dt = 3600 * 6  # 6시간으로 줄이기
steps = 5000

dt = 3600 * 24  # 시간 단계 (1일)
steps = 3000
trails = [[], [], []]  # 궤적 저장

def compute_forces(pos, mass):
	forces = np.zeros_like(pos)
	for i in range(3):
		for j in range(3):
			if i != j:
				r = pos[j] - pos[i]
				dist = np.linalg.norm(r)
				forces[i] += G * mass[i] * mass[j] / dist**2 * (r / dist)
				# 대충 중력을 계산해야겠찌?
				# 누구나 아는 중력 계산공식

	return forces

# 시뮬레이션 데이터 미리 계산
pos = positions.copy()
vel = velocities.copy()
history = []

for _ in range(steps):
	forces = compute_forces(pos, masses)
	acc = forces / masses[:, np.newaxis]
	vel += acc * dt
	pos += vel * dt
	history.append(pos.copy())

history = np.array(history)

# 애니메이션
fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(-3e11, 3e11)
ax.set_ylim(-3e11, 3e11)
ax.set_title('Three Body', color='white')

colors = ['cyan', 'orange', 'lime']
dots = [ax.plot([], [], 'o', color=c, markersize=8)[0] for c in colors]
lines = [ax.plot([], [], '-', color=c, alpha=0.4, linewidth=0.8)[0] for c in colors]

trail_len = 300

def update(frame):
	for i in range(3):
		dots[i].set_data([history[frame, i, 0]], [history[frame, i, 1]])
		start = max(0, frame - trail_len)
		lines[i].set_data(history[start:frame, i, 0], history[start:frame, i, 1])
	return dots + lines

ani = animation.FuncAnimation(fig, update, frames=steps, interval=10, blit=True)
plt.tight_layout()
plt.show()