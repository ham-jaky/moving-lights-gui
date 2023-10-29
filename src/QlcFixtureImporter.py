"""
MIT License

Copyright (c) 2023 Jakob Felix Rieckers
"""

# This has not been implemented yet

import xmltodict as xml


class NotMovingLight(Exception):
    pass


def pan_tilt_from_xml_text(xml_text):
    xml_data = xml.parse(xml_text)
    focus_data = xml_data["FixtureDefinition"]["Physical"]["Focus"]
    if not xml_data["FixtureDefinition"]["Type"] == "Moving Head":
        raise NotMovingLight
    return focus_data["@PanMax"], focus_data["@TiltMax"]


def pan_tilt_from_xml_files(xml_file):
    with open(xml_file) as f:
        pan_max, tilt_max = pan_tilt_from_xml_text(f.read())
    return pan_max, tilt_max


# From now on only tests
def main():
    print(pan_tilt_from_xml_files('../testing_area/Shehds-LED-Spot-60W-Lighting.qxf'))


if __name__ == "__main__":
    main()
