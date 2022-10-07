# cronbak.py

A python script intended to run backups as a cron job. Data is bundled into a bz2 compressed tar file.

Along with data source and destination, this script takes two additional optional arguments:
* A file prefix, useful for marking archives as weekly/monthly backups etc, or to hold backups from multiple data sources in a single directory.
* A retention size, specifying the total number of tar files of a given prefix to retain, where the oldest archives are deleted.

This script has not been extensively tested, and there are likely various edge cases and command inputs that will likely cause error. Use extreme caution and carefully test this script - it contains logic for the deletion of data.

I was looking for a simple bckup method to put into a cron job, and I had very simple requirements. Available backup scripts for this task were either to complex or didn't quite fit my needs.
