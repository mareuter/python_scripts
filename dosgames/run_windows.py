import argparse
import os
import pathlib
import subprocess as sp

TOP_DIR = pathlib.Path("~/DosGames").expanduser()
CONFIG_DIR = TOP_DIR / "config"
RUNNER = "flatpak run com.dosbox_x.DOSBox-X"
FLOPPY_525 = "-fs none -t floppy -size 512,15,2,80"
FLOPPY_35 = "-t floppy"
IMAGE_DIR = TOP_DIR / "windows"
HARD_DRIVE_PARS = "-ide 1m"
CDROM = "empty -t iso -ide 2m"
WINDOWS_UPDATES = TOP_DIR / "windows" / "updates"


def main(opts: argparse.Namespace) -> None:
    boot_config = []
    boot_conf_file = pathlib.Path("boot.conf")

    with boot_conf_file.open("w") as ofile:
        ofile.write("[autoexec]" + os.linesep)
        filine = f"{IMAGE_DIR / f'floppy{opts.floppy}.img'}"
        if opts.floppy == "35":
            fline = f"IMGMOUNT A {filine} {FLOPPY_35}"
        else:
            fline = f"IMGMOUNT A {filine} {FLOPPY_525}"
        ofile.write(fline + os.linesep)
        himg = IMAGE_DIR / f"{opts.windows}_hdd.img"
        cline = f"IMGMOUNT C {himg} {HARD_DRIVE_PARS}"
        ofile.write(cline + os.linesep)
        if opts.updates:
            dline = f"MOUNT D {WINDOWS_UPDATES / opts.windows}"
            ofile.write(dline + os.linesep)
        cd_drive = "E" if opts.updates else "D"
        cd_line = f"IMGMOUNT {cd_drive} {CDROM}"
        ofile.write(cd_line + os.linesep)
        bline = "BOOT C:"
        ofile.write(bline + os.linesep)

    boot_config.append("-conf")
    boot_config.append(boot_conf_file.name)

    cmd = RUNNER.split()

    cmd.extend(boot_config)
    cmd.append("-conf")
    cmd.append(str(CONFIG_DIR / f"{opts.windows}.conf"))

    if opts.debug:
        print(cmd)

    proc = sp.run(cmd, capture_output=True)
    if opts.debug:
        for line in proc.stdout.decode().split(os.linesep):
            print(line)

    if boot_conf_file is not None:
        boot_conf_file.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("windows", help="The flavor of windows to run.")
    parser.add_argument("--debug", dest="debug", action="store_true")
    parser.add_argument("-f", "--floppy", choices=["525", "35"], default="35",
                        help="Set the floppy drive size.")
    parser.add_argument("-u", "--updates", action="store_true", help="Mount the area for Windows updates.")

    args = parser.parse_args()
    main(args)
