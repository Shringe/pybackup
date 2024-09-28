
# pybackup
Simple python tool for backup up files and directories to another local directory. It also checks for sufficient available disk space on the filesystem of the target directory before backup up to it. 

# Configuration
Set the paths that you want to be backed up inside `pybackup/__main__.py`. Optionally set the `backup_destination` to your default backup destiation of choice. You can manually specify your `backup_destination` instead with `--backup-destination`. 

It is recommended to run the following command to test the tool before running your first backup.
```
./cli.sh --dryrun
```

# Usage
```
./cli.sh --help
```

# Installation
```bash
git clone https://github.com/Shringe/pybackup.git
cd pybackup

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
ln -s ~/path/to/here/pybackup/cli.sh ~/.local/bin/pybackup
```
