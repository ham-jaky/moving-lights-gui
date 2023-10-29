"""
MIT License

Copyright (c) 2023 Jakob Felix Rieckers

THIS IS NOT A WORKING SCRIPT THIS IS STILL IN PROGRESS USE AT YOUR OWN RISK.

This is a calculator for moving lights.
Usage: call the function Calculator.calculate()
The arguments are:
- Coordinates of the Light (xl, yl, zl)
- Coordinates of the Point you want to focus (xp, yp, zp)
- The orientation of the light (pointing to the x-axis is 0°)

The return values:
- The pan degrees (0-360)
- The tilt degrees (0-90, None)
If the tilt value is None the point is not in range
Note: The Coordinate system starts with 0; 0 at the top left corner
"""
import math


def tan_xy(x1, y1, x2, y2) -> float:
    return math.degrees(math.atan(abs(x1 - x2) / abs(y1 - y2)))


def tan_yx(x1, y1, x2, y2) -> float:
    return math.degrees(math.atan(abs(y1 - y2) / abs(x1 - x2)))


def calculate(xl, yl, zl, xp, yp, zp, orientation: float = 0):
    # Calculations for pan angle
    if xl > xp:
        if yl > yp:
            pan_angle = 90 + tan_yx(xl, yl, xp, yp)
        elif yl < yp:
            pan_angle = 0 + tan_xy(xl, yl, xp, yp)
        else:
            pan_angle = 90
    elif xl < xp:
        if yl > yp:
            pan_angle = 180 + tan_xy(xl, yl, xp, yp)
        elif yl < yp:
            pan_angle = 270 + tan_yx(xl, yl, xp, yp)
        else:
            pan_angle = 270
    else:
        if yl > yp:
            pan_angle = 180
        else:
            pan_angle = 0

    # Calculating tilt angle
    dist = math.dist([xl, yl], [xp, yp])
    if zp > zl:
        tilt_angle = math.degrees(math.atan(dist / abs(zl - zp)))
    elif zp == zl:
        tilt_angle = 90
    else:
        tilt_angle = 90 + math.degrees(math.atan(abs(zl - zp) / dist))

#    return (360-(orientation + pan_angle)) % 360, tilt_angle # the 360- is only for debugging
    return (orientation + pan_angle) % 360, tilt_angle


def angle_to_dmx_calculator(min_a, max_a, angle, has_fine: bool = True):
    if angle > max_a:
        dmx_value = 0
    elif min_a > angle:
        dmx_value = 255
    else:
        dmx_value = 255 * (angle - min_a) / (max_a - min_a)
    if has_fine:
        fine_dmx = 255 * (dmx_value % 1)
        return int(dmx_value), round(fine_dmx)
    else:
        return round(dmx_value), None


def angles_to_dmx_values(min_pan, max_pan, min_tilt, max_tilt, pan_angle, tilt_angle, has_fine: bool = True):
    pan, pan_fine = angle_to_dmx_calculator(min_pan, max_pan, pan_angle, has_fine)
    tilt, tilt_fine = angle_to_dmx_calculator(min_tilt, max_tilt, tilt_angle, has_fine)
    return pan, pan_fine, tilt, tilt_fine


def main():
    # Test (Notes.pdf for context)
    print("L1 -> P1:", calculate(1.5, 1, 3, 6, 2, 2, 0))
    print("L3 -> P3:", calculate(1.5, 5, 3, 10.5, 2, 1.8, 0))
    print("L4 -> P1:", calculate(1.5, 7, 3, 6, 2, 2, 0))
    print("L4 -> P1(h:4m):", calculate(1.5, 7, 3, 6, 2, 4, 0))
    print(angle_to_dmx_calculator(60, 300, 180))

    if input("\nDo you want to test values? [Y]\nTo cancel just press [ENTER]:\n>>>"):
        values = []
        for value in ["xl", "yl", "zl", "xp", "yp", "zp", "orientation"]:
            values.append(float(input(f"{value} >>>")))
        print(calculate(*values))


if __name__ == "__main__":
    main()
