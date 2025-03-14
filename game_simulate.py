import pygame
import math
import sys

# 초기 설정
pygame.init()
width, height = 1000, 800  # 화면 크기를 크게 설정
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("포물선 운동 시뮬레이션")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 물리 변수 설정
angle_deg = 45          # 발사각(도)
angle = math.radians(angle_deg)
velocity = 150          # 초기 속도 (픽셀/초)
gravity = 9.81          # 중력가속도
time_scale = 0.5        # 시뮬레이션 시간 배율

# 초기 위치 (왼쪽 아래, 화면의 중앙에 배치)
x0, y0 = 50, height - 50
t = 0  # 경과 시간
trajectory = []  # 궤적 저장 리스트

# 화면의 중심을 물체가 따라가게 하기 위한 시점 변수
camera_x, camera_y = x0, y0

running = True
while running:
    dt = clock.tick(60) / 1000  # 프레임 시간(초)
    t += dt / time_scale       # 시뮬레이션 시간 증가

    # 물리 공식: x = x0 + v*cos(angle)*t, y = y0 - (v*sin(angle)*t - 0.5*g*t^2)
    x = x0 + velocity * math.cos(angle) * t
    y = y0 - (velocity * math.sin(angle) * t - 0.5 * gravity * t * t)

    # 궤적 저장
    trajectory.append((int(x), int(y)))

    # 화면의 시점을 물체의 위치에 맞춰 이동
    camera_x = x - width / 2  # 화면의 중간에 물체가 오도록 시점 이동
    camera_y = y - height / 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 그리기
    screen.fill(WHITE)
    
    # 전체 궤적을 그리기
    for point in trajectory:
        # 포물선 위치를 화면의 시점에 맞춰 변환
        screen_x = point[0] - camera_x
        screen_y = point[1] - camera_y
        pygame.draw.circle(screen, RED, (screen_x, screen_y), 3)
    
    pygame.display.flip()

    # 물체가 화면을 벗어나면 더 이상 시점을 이동하지 않음
    if y > height:
        camera_x = x - width / 2
        camera_y = y - height / 2
        # 물체의 이동을 멈추고 전체 궤적을 그린 후 종료되지 않도록 설정
        running = False

# 화면이 종료되지 않고, 궤적을 계속 보이게 함
# 종료는 사용자가 직접 창을 닫을 때까지 대기
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
