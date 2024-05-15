import json


def extract_positions(config):
    positions = []
    for region_type, regions in config["cubes"]["side_regions"].items():
        for region in regions:
            position = region["coord"]
            positions.append(position)
    for region_type, regions in config["cubes"]["edge_regions"].items():
        for region in regions:
            position = region["coord"]
            positions.append(position)
    return positions


def main():
    with open("config.json") as f:
        config = json.load(f)

    positions = extract_positions(config)

    for position in positions:
        print(f"{position[0]}, {position[1]}")


if __name__ == "__main__":
    main()
