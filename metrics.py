import math

head_positions = []
hip_positions = []
speeds = []
knee_angles = []

window_size = 20

# -----------------------------
# HEAD STABILITY
# -----------------------------
def compute_head_stability(nose):
    head_positions.append(nose.x)

    if len(head_positions) > window_size:
        head_positions.pop(0)

    if len(head_positions) > 1:
        movement = 0
        for i in range(1, len(head_positions)):
            movement += abs(head_positions[i] - head_positions[i-1])

        return movement / len(head_positions)

    return 0


# -----------------------------
# ALIGNMENT (SHOULDERS)
# -----------------------------
def compute_alignment(left_shoulder, right_shoulder):
    return abs(left_shoulder.y - right_shoulder.y)


# -----------------------------
# MOMENTUM (HIP SPEED)
# -----------------------------
def compute_momentum(left_hip, right_hip):
    hip_x = (left_hip.x + right_hip.x) / 2
    hip_positions.append(hip_x)

    if len(hip_positions) > 1:
        speed = abs(hip_positions[-1] - hip_positions[-2])
        speeds.append(speed)
        return speed

    return 0


# -----------------------------
# LEG ANGLE
# -----------------------------
def compute_leg_angle(hip, knee, ankle):
    h = (hip.x, hip.y)
    k = (knee.x, knee.y)
    a = (ankle.x, ankle.y)

    v1 = (h[0] - k[0], h[1] - k[1])
    v2 = (a[0] - k[0], a[1] - k[1])

    dot = v1[0]*v2[0] + v1[1]*v2[1]

    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if mag1 == 0 or mag2 == 0:
        return 0

    angle = math.degrees(math.acos(dot / (mag1 * mag2)))
    knee_angles.append(angle)

    return angle


# -----------------------------
# 🔥 PSEUDO RELEASE FEATURES
# -----------------------------
def compute_release_features(alignment_history):
    if len(speeds) < 5 or len(knee_angles) < 5:
        return None, None, None

    # Peak momentum = release
    release_index = speeds.index(max(speeds))

    alignment_at_release = alignment_history[release_index]
    momentum_peak = speeds[release_index]

    # Leg bracing (angle increase)
    if release_index >= 3:
        before = knee_angles[release_index - 3]
    else:
        before = knee_angles[0]

    after = knee_angles[release_index]
    leg_bracing = after - before

    return alignment_at_release, momentum_peak, leg_bracing
