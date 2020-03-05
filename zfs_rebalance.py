#!/usr/bin/env python3

import os
import stat
import shutil
import sys


dry_run = False


def rebalance_path(path):
    if not os.path.isfile(path):
        return

    if os.path.islink(path):
        return

    if dry_run:
        print(path)
        return

    base_dir = os.path.dirname(path)

    saved_dir_stat = os.lstat(base_dir)
    saved_dir_mode = saved_dir_stat.st_mode

    saved_file_stat = os.lstat(path)
    saved_file_mode = saved_file_stat.st_mode

    # user id check - can't do operations below if we don't own it
    uid = os.getuid()

    if saved_dir_stat.st_uid != uid:
        print("uid mismatch on dir {}, skipping {}".format(base_dir, path))

    if saved_file_stat.st_uid != uid:
        print("uid mismatch on file {}, skipping".format(path))

    print("changing {} to 0700".format(base_dir))

    os.chmod(base_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR) # 0700

    print("changing {} to 0700".format(path))

    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR) # 0700

    counter = 1
    dst = path + ".{}".format(counter)

    while os.path.exists(dst):
        counter += 1
        dst = path + ".{}".format(counter)

    print("{} -> {}".format(path, dst))
    shutil.copy2(path, dst)

    print("rm {}".format(path))
    os.unlink(path)

    print("{} -> {}".format(dst, path))
    os.rename(dst, path)

    print("restoring mode for {}".format(path))
    os.chmod(path, saved_file_mode)
    os.utime(path, times=(saved_file_stat.st_atime,
                          saved_file_stat.st_mtime))

    print("restoring mode and times for {}".format(base_dir))
    os.chmod(base_dir, saved_dir_mode)
    os.utime(base_dir, times=(saved_dir_stat.st_atime,
                              saved_dir_stat.st_mtime))


def rebalance():
    for root, dirs, files in os.walk(sys.argv[1]):
        for name in files:
            path = os.path.join(root, name)
            rebalance_path(path)


if __name__ == "__main__":
    rebalance()

