# THREE BODY PROBLEM!!

# =========
#   UNITS
# =========
# mass → kg
# position → m (미터)
# velocity → m/s
# acceleration → m/s²
# dt → s (초)
# G → 6.674e-11 (N·m²/kg²)


import math
import numpy as np
import TBP_calculate

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
		print(value)
		self.acc = np.array(value)

	def add_accelation(self, value):
		print(value)
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
p1 = Planet(mass=1e30, position=[-1.0e11, 0.0], velocity=[1.2e4, 1.6e4], acceleration=[0.0, 0.0])
p2 = Planet(mass=1e30, position=[1.0e11, 0.0], velocity=[1.2e4, 1.6e4], acceleration=[0.0, 0.0])
p3 = Planet(mass=1e30, position=[0.0, 0.0], velocity=[-2.4e4, -3.2e4], acceleration=[0.0, 0.0])

print(p1.get_planet_data())
print(p2.get_planet_data())
print(p3.get_planet_data())

C1 = TBP_calculate.TBPCalculate(p1, p2)
p1.set_accelation(TBP_calculate.TBPCalculate(p1, p2).calculate_gravity())
p1.add_accelation(TBP_calculate.TBPCalculate(p1, p3).calculate_gravity())

p2.set_accelation(TBP_calculate.TBPCalculate(p2, p1).calculate_gravity())
p2.add_accelation(TBP_calculate.TBPCalculate(p2, p3).calculate_gravity())

p3.set_accelation(TBP_calculate.TBPCalculate(p3, p1).calculate_gravity())
p3.add_accelation(TBP_calculate.TBPCalculate(p3, p2).calculate_gravity())
print(p1.get_planet_data())
print(p2.get_planet_data())
print(p3.get_planet_data())