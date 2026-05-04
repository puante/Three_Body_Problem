# 가장 기본적인 코드 짜는 중
# 연산 관련 내용
import numpy
import math

class TBPCalculate:
	def __init__(self, p1, p2):
		self.gravity_const = 6.674e-11
		self.mass1, self.position1, self.velocity1, self.acceleration1 = p1.get_planet_data()
		self.mass2, self.position2, self.velocity2, self.acceleration2 = p2.get_planet_data()

	def get_distance(self):
		# 이건 굳이 설명 안할게요..

		# 2일차 추가 내용: 좀 수정할게 생김.
		# 거리가 0에 가까워지면 힘이 한없이 커져서 거리 최솟값을 지정하려고 함.
		return max(math.sqrt((self.position1[0] - self.position2[0]) ** 2 + (self.position1[1] - self.position2[1]) ** 2), 1e8)

	def calculate_gravity(self):
		# 행성 정보를 입력하면 1번 행성에 대해서 계산을 진행해주는 간단한(?) 함수입니다

		# 간단한 변수 지정을 해주시고요
		x1, y1 = self.position1
		x2, y2 = self.position2

		# 만유인력 공식을 통해서 값을 넣어봅시다
		force = self.gravity_const * (self.mass1 * self.mass2) / self.get_distance() ** 2

		# 이제 각도를 구해주고 (라디안 값으로 나올 거임)
		theta = math.atan2((y2 - y1), (x2 - x1))

		# 이제 저 각도를 통해 sin theta와 cos theta를 구해서 벡터룰 x, y성분으로 분해 해주면 끝입니다!
		d_fx = force * math.cos(theta)
		d_fy = force * math.sin(theta)

		# 가속도 반환
		return d_fx/self.mass1, d_fy/self.mass1

