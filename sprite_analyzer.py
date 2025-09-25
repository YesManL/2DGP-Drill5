from PIL import Image, ImageDraw, ImageFont
import os

def analyze_sprite_sheet():
    # 스프라이트 시트 로드
    sprite_sheet = Image.open('animation_sheet.png')
    width, height = sprite_sheet.size

    print(f"스프라이트 시트 크기: {width} x {height}")

    # 스프라이트 시트는 8열 4행으로 구성
    cols = 8
    rows = 4

    # 각 프레임의 크기 계산
    frame_width = width // cols
    frame_height = height // rows

    print(f"각 프레임 크기: {frame_width} x {frame_height}")

    # 프레임 좌표 정보 저장
    frame_data = []

    # 애니메이션 이름 정의
    animation_names = [
        "walk_down",   # 1행: 아래쪽 걷기
        "walk_up",     # 2행: 위쪽 걷기
        "run_right",   # 3행: 오른쪽 달리기
        "run_left"     # 4행: 왼쪽 달리기
    ]

    # 각 프레임의 좌표 계산
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height

            frame_info = {
                'animation': animation_names[row],
                'frame_index': col,
                'x': x,
                'y': y,
                'width': frame_width,
                'height': frame_height,
                'right': x + frame_width,
                'bottom': y + frame_height
            }
            frame_data.append(frame_info)

    return frame_data, sprite_sheet, frame_width, frame_height

def draw_bounding_boxes(sprite_sheet, frame_data):
    # 바운딩 박스가 그려진 이미지 생성
    result_image = sprite_sheet.copy()
    draw = ImageDraw.Draw(result_image)

    # 색상 정의 (각 애니메이션별로 다른 색상)
    colors = {
        'walk_down': '#FF0000',    # 빨간색
        'walk_up': '#00FF00',      # 초록색
        'run_right': '#0000FF',    # 파란색
        'run_left': '#FFFF00'      # 노란색
    }

    # 바운딩 박스 그리기
    for frame in frame_data:
        color = colors[frame['animation']]

        # 바운딩 박스 그리기
        draw.rectangle([
            frame['x'], frame['y'],
            frame['right']-1, frame['bottom']-1
        ], outline=color, width=2)

        # 프레임 번호 텍스트 추가
        text = f"{frame['frame_index']}"
        draw.text((frame['x']+2, frame['y']+2), text, fill=color)

    return result_image

def save_frame_info(frame_data):
    # 프레임 정보를 텍스트 파일로 저장
    with open('sprite_frame_info.txt', 'w', encoding='utf-8') as f:
        f.write("=== 스프라이트 시트 프레임 정보 ===\n\n")

        current_animation = None
        for frame in frame_data:
            if current_animation != frame['animation']:
                current_animation = frame['animation']
                f.write(f"\n[{current_animation}]\n")
                f.write("-" * 40 + "\n")

            f.write(f"프레임 {frame['frame_index']}: ")
            f.write(f"({frame['x']}, {frame['y']}) -> ({frame['right']}, {frame['bottom']}) ")
            f.write(f"크기: {frame['width']}x{frame['height']}\n")

    # Python 딕셔너리 형태로도 저장
    with open('sprite_coordinates.py', 'w', encoding='utf-8') as f:
        f.write("# 스프라이트 시트 좌표 정보\n\n")
        f.write("SPRITE_ANIMATIONS = {\n")

        current_animation = None
        for frame in frame_data:
            if current_animation != frame['animation']:
                if current_animation is not None:
                    f.write("    ],\n")
                current_animation = frame['animation']
                f.write(f"    '{current_animation}': [\n")

            f.write(f"        ({frame['x']}, {frame['y']}, {frame['width']}, {frame['height']}),  # 프레임 {frame['frame_index']}\n")

        f.write("    ]\n")
        f.write("}\n\n")

        f.write("# 사용 예시:\n")
        f.write("# x, y, width, height = SPRITE_ANIMATIONS['walk_down'][0]  # walk_down의 첫 번째 프레임\n")

def main():
    print("스프라이트 시트 분석 시작...")

    # 스프라이트 시트 분석
    frame_data, sprite_sheet, frame_width, frame_height = analyze_sprite_sheet()

    print(f"\n총 {len(frame_data)}개의 프레임 발견")
    print(f"각 프레임 크기: {frame_width} x {frame_height}")

    # 바운딩 박스가 그려진 이미지 생성
    print("\n바운딩 박스 이미지 생성 중...")
    result_image = draw_bounding_boxes(sprite_sheet, frame_data)
    result_image.save('animation_sheet_with_boxes.png')
    print("저장됨: animation_sheet_with_boxes.png")

    # 프레임 정보 저장
    print("\n프레임 정보 저장 중...")
    save_frame_info(frame_data)
    print("저장됨: sprite_frame_info.txt")
    print("저장됨: sprite_coordinates.py")

    # 콘솔에 요약 정보 출력
    print("\n=== 프레임 정보 요약 ===")
    animations = {}
    for frame in frame_data:
        if frame['animation'] not in animations:
            animations[frame['animation']] = []
        animations[frame['animation']].append(frame)

    for anim_name, frames in animations.items():
        print(f"\n{anim_name}: {len(frames)}개 프레임")
        for frame in frames:
            print(f"  프레임 {frame['frame_index']}: ({frame['x']}, {frame['y']}, {frame['width']}, {frame['height']})")

if __name__ == "__main__":
    main()
