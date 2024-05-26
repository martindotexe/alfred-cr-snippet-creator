import argparse
from os import mkdir, rename, path, walk
from shutil import copyfile, rmtree
import zipfile
from secrets import token_hex
import json
from re import search


def build_json_files(output_dir, values, prefix, suffix):
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
        output_file = path.join(
            output_dir, prefix + row[1].replace("/", "") + suffix + " [" + uid + "].json")
        with open(output_file, "w") as f:
            f.write(output)


def zip_files(output_dir):
    with zipfile.ZipFile(output_dir + ".zip", "w") as zf:
        for root, _, files in walk(output_dir):
            for f in files:
                zf.write(
                    path.join(root, f),
                    f,
                    compress_type=zipfile.ZIP_DEFLATED,
                )


def change_zip_extension(output_dir):
    renamee = output_dir + ".zip"
    pre, _ = path.splitext(renamee)
    rename(renamee, pre + ".alfredsnippets")


def collect_files(input_dir):
    data = {}
    for root, _, files in walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                with open(path.join(root, file)) as f:
                    data[file] = [tuple(line.strip().split("\t"))
                                  for line in f.readlines()
                                  if bool(search(r".+\t.+", line))]
    return data


def main(input_dir, output_dir, prefix, suffix):
    file_data = collect_files(input_dir)
    for key, values in file_data.items():
        file_name = path.join(output_dir, key.replace(".txt", ""))
        mkdir(file_name)
        copyfile("info.plist", path.join(file_name, "info.plist"))
        build_json_files(file_name, values, prefix, suffix)
        zip_files(file_name)
        change_zip_extension(file_name)
        rmtree(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Alfred snippets from text files.")
    parser.add_argument("input_dir", help="Directory containing text files")
    parser.add_argument(
        "output_dir", help="Directory to save the output files")
    parser.add_argument("--prefix", default="",
                        help="Prefix to add to the filenames")
    parser.add_argument("--suffix", default="",
                        help="Suffix to add to the filenames")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.prefix, args.suffix)
