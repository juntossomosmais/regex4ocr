"""
Main script to invoke json4ocr.
"""
import argparse
import io
import os

from google.cloud import vision


def detect_text(path):
    """
    Detects text in the file.

    [!] DOCUMENT TEXT detection != TEXT DETECTION ONLY.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # response = client.text_detection(image=image)
    response = client.document_text_detection(image=image)

    texts = response.text_annotations

    return texts


def parse_args():
    """
    Parses user arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--auth", default="./auth.json")
    parser.add_argument("-i", "--image", required=True)
    parser.add_argument("-d", "--debug", default=None, nargs="?", const=True)
    args = vars(parser.parse_args())

    return args


def main():
    """ Main function of json4ocr. """
    args = parse_args()
    img_path = args.get("image")
    auth_json_path = args.get("auth")

    # sets auth env variable to use Google Vision API
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_json_path

    texts = detect_text(img_path)
    ocr_result = texts[0].description

    if args.get("debug"):
        os.environ["LOGGING_LEVEL"] = "DEBUG"

    # Python imports json4ocr module after the logging_level has been set
    from json4ocr import json4ocr

    json4ocr(ocr_result)


if __name__ == "__main__":
    main()
