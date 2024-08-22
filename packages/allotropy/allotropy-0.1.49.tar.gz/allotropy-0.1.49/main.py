import json
from pathlib import Path

from allotropy.constants import CHARDET_ENCODING
from allotropy.parser_factory import Vendor
from allotropy.to_allotrope import allotrope_from_file

output_files = [
    "group_cols_with_int_sample_names.txt",
    # "SEAP_SPECTRAMAX_D1_PLATE 2 (3).txt",
    # "SEAP!_SPECTRAMAX_D1_PLATE 1 (3).txt",
]
vendor = Vendor.MOLDEV_SOFTMAX_PRO


if __name__ == "__main__":
    # filename = "Beckman_Vi-Cell-XR_example02_instrumentOutput.xls"
    for filename in output_files:
        # read_mode = "fluorescence"
        # test_filepath = (
        #     f"tests/parsers/agilent_gen5/testdata/{read_mode}/{filename}.txt"
        # )
        # test_filepath = f"tests/parsers/luminex_xponent/testdata/{filename}.csv"
        test_filepath = f"{filename}"

        allotrope_dict = allotrope_from_file(
            test_filepath, vendor, encoding=CHARDET_ENCODING
        )
        target_filename = Path(test_filepath).with_suffix(".json").name
        # print(allotrope_dict)
        with open(target_filename, "w") as fp:
            fp.write(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))
