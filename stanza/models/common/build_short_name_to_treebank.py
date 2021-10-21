import glob
import os

from stanza.models.common.constant import treebank_to_short_name
from stanza.utils import default_paths

paths = default_paths.get_default_paths()
udbase = paths["UDBASE"]

directories = glob.glob(udbase + "/UD_*")
directories.sort()

output_name = os.path.join(os.path.split(__file__)[0], "short_name_to_treebank.py")
with open(output_name, "w") as fout:
    fout.write("# This module is autogenerated by build_short_name_to_treebank.py\n")
    fout.write("# Please do not edit\n")
    fout.write("\n")
    fout.write("SHORT_NAMES = {\n")
    for ud_path in directories:
        ud_name = os.path.split(ud_path)[1]
        short_name = treebank_to_short_name(ud_name)
        fout.write("    '%s': '%s',\n" % (short_name, ud_name))

        if short_name.startswith("zh_"):
            short_name = "zh-hans_" + short_name[3:]
            fout.write("    '%s': '%s',\n" % (short_name, ud_name))

    fout.write("}\n")

    fout.write(
        """

def short_name_to_treebank(short_name):
    return SHORT_NAMES[short_name]
"""
    )
