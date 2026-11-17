import argparse
import cv2

from config import EVIDENCE_DIR, INPUT_VIDEO
from run_manifest import load_verified_run_manifest
from zone import draw_zone, get_zone_polygon


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    args = parser.parse_args()

    manifest_path = (
        EVIDENCE_DIR / args.run_id / "manifest.json"
    )

    manifest = load_verified_run_manifest(
        manifest_path=manifest_path,
        input_video=INPUT_VIDEO,
        expected_run_id=args.run_id,
    )

    video_info = manifest["input_video"]


    capture = cv2.VideoCapture(str(INPUT_VIDEO))

    if not capture.isOpened():
        raise RuntimeError("Cannot open input video.")

    try:
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        if (
            [width, height] != video_info["resolution"]
            or total_frames != video_info["total_frames"]
            or total_frames < 1
        ):
            raise ValueError("Video metadata does not match manifest.")

        polygon = get_zone_polygon(
            width,
            height,
            manifest["zone_config"]["normalized_points"],
        )

        scale = min(960 / width, 540 / height, 1.0)
        display_size = (
            round(width * scale),
            round(height * scale),
        )

        frame_index = 0
        window = "ZoneTrace - Ground Truth Viewer"

        print("A/D: Previous/next frame")
        print("J/L: Back/forward 10 frames")
        print("Q or ESC: Quit")

        while True:
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = capture.read()

            if not success:
                raise RuntimeError(
                    f"Cannot read frame {frame_index + 1}."
                )

            draw_zone(frame, polygon)

            cv2.rectangle(
                frame, (0, 0), (width, 42), (0, 0, 0), -1
            )

            cv2.putText(
                frame,
                f"Frame {frame_index + 1}/{total_frames}",
                (15, 29),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            preview = cv2.resize(frame, display_size)
            cv2.imshow(window, preview)

            key = cv2.waitKey(0) & 0xFF

            if key in (ord("q"), 27):
                break
            elif key == ord("d"):
                frame_index = min(frame_index + 1, total_frames - 1)
            elif key == ord("a"):
                frame_index = max(frame_index - 1, 0)
            elif key == ord("l"):
                frame_index = min(frame_index + 10, total_frames - 1)
            elif key == ord("j"):
                frame_index = max(frame_index - 10, 0)

    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()