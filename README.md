"Rebalance" files on a ZFS file system by

1. Copying them to a different file name
1. Deleting the original copy
1. Renaming the different file name to the original

This script also automatically sets the approprite file and directory
permissions so that the above steps can complete. After the last step, the
original permissions are restored.

The primary use of this script is to spread blocks around equally in a zpool.
If a new vdev is added to an existing pool, it initially doesn't have any
blocks. Read and writes are round-robin spread between the vdevs in a pool, and . If the
original vdevs were close to capacity then this isn't possible so the blocks are
written to the new vdev.

Here is an example of an unbalanced zpool:

    $ sudo zpool list -v
    NAME                                           SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
    pool                                          18.2T  6.85T  11.3T        -         -     0%    37%  1.00x    ONLINE  -
      mirror                                      7.27T  4.57T  2.69T        -         -     0%  62.9%      -  ONLINE
        ata-HGST_HDN728080ALE604_R6G9PUEY             -      -      -        -         -      -      -      -  ONLINE
        ata-ST8000DM004-2CX188_ZCT0EM3Y               -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T  1.13T   702G        -         -     0%  62.2%      -  ONLINE
        ata-WDC_WD20EARS-00MVWB0_WD-WMAZA0686209      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300563174      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T  1.15T   675G        -         -     0%  63.6%      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300578369      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M2UHLZ54      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      7.27T   196K  7.27T        -         -     0%  0.00%      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_1EHWA06Z             -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_2SGARPHJ             -      -      -        -         -      -      -      -  ONLINE

In this case, I had an existing pool with 8tb + 2tb + 2tb vdevs, and added
another 8tb vdev. Initially, the new 8tb vdev is blank, and the whole pool had
6.9T used and 11T available. The three original vdevs had roughly the same
capacity used.

After running this script once on the mountpoint of the pool:

    $ sudo zpool list -v
    NAME                                           SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
    pool                                          18.2T  6.85T  11.3T        -         -     0%    37%  1.00x    ONLINE  -
      mirror                                      7.27T  2.34T  4.93T        -         -     0%  32.2%      -  ONLINE
        ata-HGST_HDN728080ALE604_R6G9PUEY             -      -      -        -         -      -      -      -  ONLINE
        ata-ST8000DM004-2CX188_ZCT0EM3Y               -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T   658G  1.17T        -         -     0%  35.4%      -  ONLINE
        ata-WDC_WD20EARS-00MVWB0_WD-WMAZA0686209      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300563174      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T   658G  1.17T        -         -     0%  35.4%      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300578369      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M2UHLZ54      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      7.27T  3.23T  4.04T        -         -     0%  44.4%      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_1EHWA06Z             -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_2SGARPHJ             -      -      -        -         -      -      -      -  ONLINE

And again:

    $ sudo zpool list -v
    NAME                                           SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
    pool                                          18.2T  6.87T  11.3T        -         -     0%    37%  1.00x    ONLINE  -
      mirror                                      7.27T  2.78T  4.48T        -         -     0%  38.3%      -  ONLINE
        ata-HGST_HDN728080ALE604_R6G9PUEY             -      -      -        -         -      -      -      -  ONLINE
        ata-ST8000DM004-2CX188_ZCT0EM3Y               -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T   758G  1.07T        -         -     1%  40.9%      -  ONLINE
        ata-WDC_WD20EARS-00MVWB0_WD-WMAZA0686209      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300563174      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      1.81T   759G  1.07T        -         -     1%  40.9%      -  ONLINE
        ata-WDC_WD20EFRX-68AX9N0_WD-WMC300578369      -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M2UHLZ54      -      -      -        -         -      -      -      -  ONLINE
      mirror                                      7.27T  2.61T  4.66T        -         -     0%  35.9%      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_1EHWA06Z             -      -      -        -         -      -      -      -  ONLINE
        ata-WDC_WD80EMAZ-00WJTA0_2SGARPHJ             -      -      -        -         -      -      -      -  ONLINE

Each run was approximately:

    real    2794m28.111s
    user    36m42.898s
    sys     120m59.941s

or 46.5 hours.

Note that deduplication has to be off for this rebalance to work. As well, if
you do a snapshot before this, expect to require enough disk space to hold an
entirely new set of blocks. But that's the point, because the aim of this tool
is to force new blocks to be created :).

