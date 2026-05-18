from pathlib import Path


def collect_image_paths(root_dir: Path) -> list[tuple[Path, str]]:
    items: list[tuple[Path, str]] = []
    for class_dir in sorted(root_dir.iterdir()):
        if not class_dir.is_dir():
            continue

        for image_path in sorted(class_dir.glob("*.png")):
            items.append((image_path, class_dir.name))

    return items


def collect_image_paths_from_roots(root_dirs: list[Path]) -> list[tuple[Path, str]]:
    items: list[tuple[Path, str]] = []
    for root_dir in root_dirs:
        items.extend(collect_image_paths(root_dir))
    return sorted(items, key=lambda item: (item[1], str(item[0])))
