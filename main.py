import cv2

from pose_detection import get_pose, draw_pose
from data_extraction import extract_keypoints
from metrics import (
    compute_head_stability,
    compute_alignment,
    compute_momentum,
    compute_leg_angle,
    compute_release_features,
    head_positions
)
from data_logger import log_data, save_data, clear_data

#  Start fresh every run
clear_data()

cap = cv2.VideoCapture(0)

# Store alignment history
alignment_history = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = get_pose(frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        keypoints = extract_keypoints(landmarks)

        # ==============================
        # 🔹 HEAD STABILITY
        # ==============================
        head = compute_head_stability(keypoints["nose"])

        # ==============================
        # 🔹 ALIGNMENT
        # ==============================
        align = compute_alignment(
            keypoints["left_shoulder"],
            keypoints["right_shoulder"]
        )
        alignment_history.append(align)

        # ==============================
        # 🔹 MOMENTUM
        # ==============================
        momentum = compute_momentum(
            keypoints["left_hip"],
            keypoints["right_hip"]
        )

        # ==============================
        # 🔹 FRONT LEG DETECTION + ANGLE
        # ==============================
        if keypoints["left_ankle"].y > keypoints["right_ankle"].y:
            leg_angle = compute_leg_angle(
                keypoints["left_hip"],
                keypoints["left_knee"],
                keypoints["left_ankle"]
            )
            leg_label = "Left Leg"
        else:
            leg_angle = compute_leg_angle(
                keypoints["right_hip"],
                keypoints["right_knee"],
                keypoints["right_ankle"]
            )
            leg_label = "Right Leg"

        # ==============================
        # 🔹 DISPLAY (LIVE METRICS)
        # ==============================

        # Head stability
        head_color = (0, 255, 0) if head < 0.02 else (0, 0, 255)
        cv2.putText(frame, f"Head: {head:.3f}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, head_color, 2)

        # Alignment
        align_color = (0, 255, 0) if align < 0.02 else (0, 0, 255)
        cv2.putText(frame, f"Align: {align:.3f}", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, align_color, 2)

        # Momentum
        cv2.putText(frame, f"Momentum: {momentum:.3f}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Leg angle (LIVE only, not bracing)
        leg_color = (0, 255, 0) if leg_angle > 160 else (0, 0, 255)
        cv2.putText(frame, f"{leg_label}: {leg_angle:.1f}", (30, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, leg_color, 2)

        # Draw skeleton
        draw_pose(frame, results)

    else:
        cv2.putText(frame, "Pose Not Detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show frame
    cv2.imshow("Bowling Analysis", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==============================
#  AFTER RECORDING (FINAL FEATURES)
# ==============================

align_release, momentum_peak, leg_bracing = compute_release_features(alignment_history)

if align_release is not None:
    avg_head = sum(head_positions) / len(head_positions)

    print("\n=== FINAL DELIVERY FEATURES ===")
    print(f"Head Stability: {avg_head:.4f}")
    print(f"Alignment (at release): {align_release:.4f}")
    print(f"Momentum (peak): {momentum_peak:.4f}")
    print(f"Leg Bracing: {leg_bracing:.2f}")

    # Log ONE row
    log_data(avg_head, align_release, momentum_peak, leg_bracing)

    # Save CSV
    save_data()

else:
    print("\nNot enough data collected. Record longer.")

cap.release()
cv2.destroyAllWindows()
