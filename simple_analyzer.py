import os
from PIL import Image, ImageDraw

# 현재 디렉토리 확인
print("현재 작업 디렉토리:", os.getcwd())

# 스프라이트 시트 파일이 있는지 확인
if os.path.exists('animation_sheet.png'):
    print("animation_sheet.png 파일을 찾았습니다.")

    # 이미지 로드
    sprite_sheet = Image.open('animation_sheet.png')
    width, height = sprite_sheet.size
    print(f"스프라이트 시트 크기: {width} x {height} 픽셀")

    # 8x4 그리드로 분할
    cols, rows = 8, 4
    frame_width = width // cols
    frame_height = height // rows

    print(f"각 프레임 크기: {frame_width} x {frame_height} 픽셀")
    print(f"총 프레임 수: {cols * rows}개")

    # 프레임 좌표 계산 및 출력
    print("\n=== 프레임 좌표 정보 ===")

    animation_names = ["walk_down", "walk_up", "run_right", "run_left"]

    for row in range(rows):
        print(f"\n{animation_names[row]} (행 {row+1}):")
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            print(f"  프레임 {col}: ({x}, {y}, {frame_width}, {frame_height}) - 오른쪽하단: ({x + frame_width}, {y + frame_height})")

    # 바운딩 박스가 그려진 이미지 생성
    result_image = sprite_sheet.copy()
    draw = ImageDraw.Draw(result_image)

    colors = ['red', 'green', 'blue', 'yellow']

    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height

            # 바운딩 박스 그리기
            draw.rectangle([x, y, x + frame_width - 1, y + frame_height - 1],
                         outline=colors[row], width=2)

            # 프레임 번호 표시
            draw.text((x + 2, y + 2), str(col), fill=colors[row])

    # 결과 이미지 저장
    result_image.save('animation_sheet_with_bounding_boxes.png')
    print(f"\n바운딩 박스가 그려진 이미지가 'animation_sheet_with_bounding_boxes.png'로 저장되었습니다.")

else:
    print("animation_sheet.png 파일을 찾을 수 없습니다.")
    print("현재 디렉토리의 파일 목록:")
    for file in os.listdir('.'):
        print(f"  {file}")
