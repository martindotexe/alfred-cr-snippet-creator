from os import mkdir, rename, path, walk
from shutil import copyfile, rmtree
import zipfile
from secrets import token_hex
import json

RESULT_COLLECTION_NAME = "My New Snippet Collection"


def build_json_files():
    source_file = "snippets.txt"

    with open(source_file, newline='', encoding="utf-8-sig") as file:
        rows = [line.split("\t") for line in file.readlines()]
        for row in rows:
            uid = token_hex(15)
            output = json.dumps(
                {
                    "alfredsnippet": {
                        "snippet": row[1],
                        "uid": uid,
                        "keyword": row[0],
                        "name": row[1],
                    },
                },
                sort_keys=False,
                indent=4,
                separators=(',', ': '),
            )
            output_file = RESULT_COLLECTION_NAME + \
                "/" + row[1].replace("/", "") + " [" + uid + "].json"
            with open(output_file, "w") as f:
                f.write(output)


def zip_files():
    with zipfile.ZipFile(RESULT_COLLECTION_NAME + ".zip", "w") as zf:
        for root, _, files in walk(RESULT_COLLECTION_NAME):
            for f in files:
                zf.write(
                    path.join(root, f),
                    f,
                    compress_type=zipfile.ZIP_DEFLATED,
                )


def change_zip_extension():
    renamee = RESULT_COLLECTION_NAME + ".zip"
    pre, _ = path.splitext(renamee)
    rename(renamee, pre + ".alfredsnippets")


mkdir(RESULT_COLLECTION_NAME)
copyfile("./info.plist", "./" + RESULT_COLLECTION_NAME + "/info.plist")
build_json_files()
zip_files()
change_zip_extension()
rmtree(RESULT_COLLECTION_NAME)
