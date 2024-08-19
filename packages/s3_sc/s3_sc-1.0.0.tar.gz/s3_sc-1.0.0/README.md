# Python s3 client

Simple object client for any bucket like s3.

# Usage

Install from pypi

```bash
pip3 install s3_sc
```

Local

```bash
poetry install
```

Run

```bash
s3_sc -c <s3_config> ls / - listing root.
s3_sc -c <s3_config> ls /<dir>/ - listing object inside specific dir.

s3_sc -c <s3_config> put <path_to_local_file> /<path_in_s3>

s3_sc -c <s3_config> delete <path_to_file> or <path_to_dir/> (with / in the end)

s3_sc -c <s3_config> get <path_to_s3_file> <path_to_local_save>
```
