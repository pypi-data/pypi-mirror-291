import argparse
from .tpl_reader import TPLReader


def main():
    parser = argparse.ArgumentParser(description="Parse Photoshop TPL files and save the output as JSON.")

    parser.add_argument(
        "input_file",
        help="Path to the TPL file to be parsed."
    )

    parser.add_argument(
        "-o", "--output",
        default="output.json",
        help="Path to save the parsed JSON data. Defaults to 'output.json'."
    )

    args = parser.parse_args()

    tpl_reader = TPLReader(args.input_file)
    tpl_reader.read_tpl()
    tpl_reader.save_to_json(args.output)

    print(f"Parsed TPL data has been saved to {args.output}")


if __name__ == "__main__":
    main()
