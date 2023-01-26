from argparse import ArgumentParser

from PIL import Image, ImageSequence

from conformal import Spiral
from tiled import apply_map


def main():
    parser = ArgumentParser(description="Apply conformal maps to images")

    parser.add_argument("file", metavar="file", nargs=1, help="The image to map")

    parser.add_argument("-o", "--output", metavar="output", nargs="?", default=None)

    parser.add_argument("-r", "--resolution", nargs="?", default="512:512")

    args = parser.parse_args()

    input_file = args.file[0]
    output_file = args.output or "output.png"

    resolution = tuple(map(int, args.resolution.split(":")))

    input_image = Image.open(input_file)

    conformal_map = Spiral(input_image.height, input_image.width)
    #conformal_map = Mobius_Inverse(1, -1j, 1, 1j)

    if input_image.format == "GIF":
        # Currently produces bloated files, the linear
        # interpolation does not like working with a
        # a palette so this does everything in rgb
        # at the end should realy convert to a palette
        # again to save space
        frames = []

        input_frames = ImageSequence.Iterator(input_image)
        for index, frame in enumerate(input_frames, start=1):
            print(f"\rComputing frame: {index}", end="")
            output = apply_map(frame, resolution, conformal_map)
            frames.append(output)

        print()

        # All of this just facilitates animation
        # Save every frame one after the other
        # Loop forever
        # 33 miliseconds per frame: 30fps
        frames[0].save(
            output_file, save_all=True, append_images=frames[1:], loop=0, duration=33
        )
    else:
        apply_map(input_image, resolution, conformal_map).save(output_file)

    print("done")


if __name__ == "__main__":
    main()
