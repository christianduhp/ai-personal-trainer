# Lógica de flexões
def pushup(status, count, elbow_angle, hip_angle, direction):

    def is_elbow_ready(elbow_angle):
        return elbow_angle > 150

    def is_elbow_down(elbow_angle):
        return 50 < elbow_angle < 80

    def is_elbow_up(elbow_angle):
        return 120 < elbow_angle < 180

    def is_hip_straight(hip_angle):
        return hip_angle > 100

    if is_elbow_ready(elbow_angle) and is_hip_straight(hip_angle):
        status = "ready"
        direction = "down"

    if status == "ready":
        if direction == "down" and is_elbow_down(elbow_angle):
            direction = "up"
            count += 0.5
        elif direction == "up" and is_elbow_up(elbow_angle):
            direction = "down"
            count += 0.5
    return status, count, direction
