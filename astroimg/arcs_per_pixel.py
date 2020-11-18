import argparse

import astropy.units as u
import yaml


def make_quantity(values):
    return float(values[0]) * u.Unit(values[1])


def main(opts):
    with open("camera_info.yaml") as ifile:
        cameras = yaml.safe_load(ifile)

    focal_length = make_quantity(opts.focal_length)

    for camera in cameras:
        if camera["manufacturer"] == opts.camera_maker and camera["model"] == opts.camera_model:
            sensor_width = make_quantity(camera["sensor_width"].split())
            sensor_height = make_quantity(camera["sensor_height"].split())

            pixel_size_width = sensor_width / camera["pixel_width"]
            pixel_size_height = sensor_height / camera["pixel_height"]

            pixel_size = (pixel_size_width + pixel_size_height) / 2
            if opts.show_size:
                print(f"Pixel Size: {pixel_size.to(u.Unit(opts.size_units)):.4f}")

            pixel_scale = (pixel_size * (205920 * u.arcsec)) / focal_length
            print(f"Pixel Scale: {pixel_scale:.4f} per pixel")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_maker", help="The camera manufacturer.")
    parser.add_argument("camera_model", help="The camera model.")
    parser.add_argument("focal_length", nargs=2, help="Focal length including units: 130 mm.")
    parser.add_argument("--show-size", action="store_true", help="Show the size of a pixel.")
    parser.add_argument("--size-units", default="um", help="Set the untis for the pixel size.")

    args = parser.parse_args()
    main(args)
