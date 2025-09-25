from pico2d import *


TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

# 각 애니메이션별 프레임 좌표 (x, y, width, height)
SPRITE_ANIMATIONS = {
    'run_left': [
        (0, 0, 100, 100),      # 프레임 0
        (100, 0, 100, 100),    # 프레임 1
        (200, 0, 100, 100),    # 프레임 2
        (300, 0, 100, 100),    # 프레임 3
        (400, 0, 100, 100),    # 프레임 4
        (500, 0, 100, 100),    # 프레임 5
        (600, 0, 100, 100),    # 프레임 6
        (700, 0, 100, 100),    # 프레임 7
    ],
    'run_right': [
        (0, 100, 100, 100),    # 프레임 0
        (100, 100, 100, 100),  # 프레임 1
        (200, 100, 100, 100),  # 프레임 2
        (300, 100, 100, 100),  # 프레임 3
        (400, 100, 100, 100),  # 프레임 4
        (500, 100, 100, 100),  # 프레임 5
        (600, 100, 100, 100),  # 프레임 6
        (700, 100, 100, 100),  # 프레임 7
    ],
    'walk_right': [
        (0, 200, 100, 100),    # 프레임 0
        (100, 200, 100, 100),  # 프레임 1
        (200, 200, 100, 100),  # 프레임 2
        (300, 200, 100, 100),  # 프레임 3
        (400, 200, 100, 100),  # 프레임 4
        (500, 200, 100, 100),  # 프레임 5
        (600, 200, 100, 100),  # 프레임 6
        (700, 200, 100, 100),  # 프레임 7
    ],
    'walk_left': [
        (0, 300, 100, 100),    # 프레임 0
        (100, 300, 100, 100),  # 프레임 1
        (200, 300, 100, 100),  # 프레임 2
        (300, 300, 100, 100),  # 프레임 3
        (400, 300, 100, 100),  # 프레임 4
        (500, 300, 100, 100),  # 프레임 5
        (600, 300, 100, 100),  # 프레임 6
        (700, 300, 100, 100),  # 프레임 7
    ]
}

def handle_events():
    global running, x_dir, y_dir

    global x, y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                x_dir += 1
            elif event.key == SDLK_LEFT:
                x_dir -= 1
            elif event.key == SDLK_UP:
                y_dir += 1
            elif event.key == SDLK_DOWN:
                y_dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                x_dir -= 1
            elif event.key == SDLK_LEFT:
                x_dir += 1
            elif event.key == SDLK_UP:
                y_dir -= 1
            elif event.key == SDLK_DOWN:
                y_dir += 1


def get_current_animation(x_dir, y_dir, last_direction):
    """현재 이동 방향에 따라 적절한 애니메이션을 반환"""
    if x_dir > 0:  # 오른쪽으로 이동
        return 'run_right'
    elif x_dir < 0:  # 왼쪽으로 이동
        return 'run_left'
    elif y_dir != 0:  # 위/아래로 이동
        # 위/아래 이동시 이전 방향에 따라 run 애니메이션 선택
        if last_direction > 0:  # 이전에 오른쪽으로 이동했었다면
            return 'run_right'
        elif last_direction < 0:  # 이전에 왼쪽으로 이동했었다면
            return 'run_left'
        else:  # 초기 상태에서 위/아래 이동
            return 'run_right'  # 기본값
    else:  # 정지 상태
        # 이전 방향에 따라 적절한 walk 애니메이션 선택
        if last_direction > 0:  # 이전에 왼쪽으로 이동
            return 'walk_left'
        elif last_direction < 0:  # 이전에 오른쪽으로 이동
            return 'walk_right'
        else:  # 초기 상태
            return 'walk_right'  # 기본값

def update_character(x, y, frame, x_dir, y_dir, last_direction):
    """캐릭터를 현재 상태에 맞게 화면에 그리기"""
    animation = get_current_animation(x_dir, y_dir, last_direction)
    sprite_x, sprite_y, sprite_width, sprite_height = SPRITE_ANIMATIONS[animation][frame]
    character.clip_draw(sprite_x, sprite_y, sprite_width, sprite_height, x, y)

global running, x_dir, y_dir

running = True
x = 800 // 2
y = 800 // 2
frame = 0
x_dir = 0
y_dir = 0
last_x_dir = 0  # 이전 x 방향을 추적하는 변수

while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 캐릭터 업데이트 및 그리기
    update_character(x, y, frame, x_dir, y_dir, last_x_dir)

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    x += x_dir * 5
    y += y_dir * 5

    # 이전 방향 업데이트 (x축으로 이동 중일 때만)
    if x_dir != 0:
        last_x_dir = x_dir

    delay(0.05)

close_canvas()
