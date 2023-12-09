from os import mkdir, rename, path, walk
from shutil import copyfile, rmtree
import zipfile
from secrets import token_hex
import csv
import json

RESULT_COLLECTION_NAME = "My New Snippet Collection"


def build_json_files(file_name, values):
    for row in values:
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
        output_file = file_name + \
            "/" + row[1].replace("/", "") + " [" + uid + "].json"
        with open(output_file, "w") as f:
            f.write(output)


def zip_files(file_name):
    with zipfile.ZipFile(file_name + ".zip", "w") as zf:
        for root, _, files in walk(file_name):
            for f in files:
                zf.write(
                    path.join(root, f),
                    f,
                    compress_type=zipfile.ZIP_DEFLATED,
                )


def change_zip_extension(file_name):
    renamee = file_name + ".zip"
    pre, _ = path.splitext(renamee)
    rename(renamee, pre + ".alfredsnippets")


def collect_files():
    data = {}
    for root, _, files in walk("files"):
        for file in files:
            if file.endswith(".txt"):
                with open(f"{root}/{file}") as f:
                    data[file] = [tuple(line.strip().split("\t"))
                                  for line in f.readlines()]
    return data


file_data = collect_files()
for key, values in file_data.items():
    file_name = f'cr/{key.replace(".txt", "")}'
    mkdir(file_name)
    copyfile("./info.plist", "./" + file_name + "/info.plist")
    build_json_files(file_name, values)
    zip_files(file_name)
    change_zip_extension(file_name)
    rmtree(file_name)
