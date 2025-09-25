from PIL import Image, ImageDraw
import os

def create_bounding_box_image():
    """animation_sheet.png에 바운딩 박스를 그려서 새 이미지로 저장"""

    # 원본 이미지 로드
    try:
        sprite_sheet = Image.open('animation_sheet.png')
        print(f"이미지 로드 성공: {sprite_sheet.size}")
    except Exception as e:
        print(f"이미지 로드 실패: {e}")
        return

    width, height = sprite_sheet.size

    # 8x4 그리드로 계산
    cols, rows = 8, 4
    frame_width = width // cols
    frame_height = height // rows

    print(f"계산된 프레임 크기: {frame_width} x {frame_height}")

    # 복사본 생성
    result_image = sprite_sheet.copy()
    draw = ImageDraw.Draw(result_image)

    # 각 행별 색상
    colors = ['red', 'lime', 'blue', 'yellow']
    animation_names = ['walk_down', 'walk_up', 'run_right', 'run_left']

    # 바운딩 박스 그리기
    for row in range(rows):
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height

            # 바운딩 박스 사각형
            draw.rectangle(
                [x, y, x + frame_width - 1, y + frame_height - 1],
                outline=colors[row],
                width=2
            )

            # 프레임 번호 텍스트
            draw.text(
                (x + 3, y + 3),
                f"{col}",
                fill=colors[row]
            )

            # 애니메이션 이름 (첫 번째 프레임에만)
            if col == 0:
                draw.text(
                    (x + 3, y + frame_height - 15),
                    animation_names[row][:4],
                    fill=colors[row]
                )

    # 결과 저장
    result_image.save('animation_sheet_with_bounding_boxes.png')
    print("바운딩 박스 이미지 저장 완료: animation_sheet_with_bounding_boxes.png")

    return frame_width, frame_height

if __name__ == "__main__":
    create_bounding_box_image()
