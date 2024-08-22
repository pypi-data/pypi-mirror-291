from typing import List, Tuple

from tenyks_sdk.sdk.tag import Tag


def string_to_tag_name_and_value(
    tag_string: str, tag_names: List[str]
) -> Tuple[str, str]:
    # Sort list of strings, longest first, to ensure correct parsing
    tag_names.sort(key=len, reverse=True)
    for tag_name in tag_names:
        if tag_string.startswith(tag_name):
            tag_value = tag_string.replace(f"{tag_name}_", "")
            return tag_name, tag_value
    raise ValueError(f"Tag {tag_string} not found in dataset tags")


def strings_to_tags(tag_strings: List[str], dataset_tags: List[Tag]) -> List[Tag]:
    tag_names = [tag.name for tag in dataset_tags]
    tag_dict = {tag.name: [] for tag in dataset_tags}

    for tag_string in tag_strings:
        tag_name, tag_value = string_to_tag_name_and_value(tag_string, tag_names)
        tag_dict[tag_name].append(tag_value)

    return [
        Tag(key=name, name=name, values=values)
        for name, values in tag_dict.items()
        if values
    ]
