from mouselungseg import LungsPredictor
import tifffile
from pathlib import Path
import argparse
import glob


def process_input_file_predict(input_image_file, predictor):
    image = tifffile.imread(input_image_file)

    segmentation = predictor.predict(image)

    pt = Path(input_image_file)
    out_file_name = pt.parent / f"{pt.stem}_mask.tif"

    tifffile.imwrite(out_file_name, segmentation)

    print("Wrote to ", out_file_name)


def cli_predict_image():
    """Command-line entry point for model inference."""
    parser = argparse.ArgumentParser(description="Use this command to run inference.")
    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="Input image. Must be a TIF image file.",
    )
    args = parser.parse_args()

    input_image_file = args.i

    predictor = LungsPredictor()

    process_input_file_predict(input_image_file, predictor)


def cli_predict_folder():
    parser = argparse.ArgumentParser(
        description="Use this command to run inference in batch on a given folder."
    )
    parser.add_argument(
        "-i",
        type=str,
        required=True,
        help="Input folder. Must contain suitable TIF image files.",
    )
    args = parser.parse_args()

    input_folder = args.i

    lungs_predict = LungsPredictor()

    for input_image_file in glob.glob(str(Path(input_folder) / "*.tif")):
        process_input_file_predict(input_image_file, lungs_predict)
