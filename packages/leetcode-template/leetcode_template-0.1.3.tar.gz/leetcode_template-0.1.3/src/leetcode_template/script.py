from . import generate_template
import argparse


parser = argparse.ArgumentParser(
    prog="Leetcode Template", description="Generating Leetcode Templates for c++"
)

parser.add_argument(
    "-s",
    "--signature",
    help="Path to the signature file",
    required=False,
    default="signature.json",
)

args = parser.parse_args()


def main():
    generate_template.main(args.signature)


if __name__ == "__main__":
    main()
