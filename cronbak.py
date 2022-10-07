#!/usr/bin/env python3

from datetime import datetime
import glob
import tarfile
import os
import argparse
import pathlib



def timestring():
    
    return datetime.today().strftime("%Y-%m-%d_%H-%M-%S")



def gen_name(prefix=None):
    
    prefix='' if not prefix or prefix=='' else prefix+'_'
    
    return prefix+timestring()+'.tar.bz2'



def get_archives(location, prefix=None):
    
    prefix='' if not prefix or prefix=='' else prefix+'_'
    
    timestring_glob="[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]"
    
    return glob.glob(location+'/'+prefix+timestring_glob+'.tar.bz2')



def create_archive(source, destination, prefix=None):
    
    name = destination+'/'+gen_name(prefix)
    
    with tarfile.open(name=name, mode='w:bz2') as tf:
        tf.add(source)
    
    os.chmod(name, 0o400)
    
    return name



def prune_backups(location, prefix=None, max_retention=None):
    
    if max_retention==None:
        return

    archives=sorted(get_archives(location, prefix), reverse=True)
    
    while len(archives)>max_retention:
        
        name = archives.pop()
        
        print("Deleting backup: "+name)
        
        os.remove( name )
    
    return



def run_backup(source, destination, prefix=None, max_retention=None):
    
    create_archive(source, destination, prefix)
    
    if max_retention:
        prune_backups(destination, prefix, max_retention)
    
    return



def build_parser():
    
    parser = argparse.ArgumentParser(
        description="A file backup utility script intended for the cron table.",
        epilog="Richard Morrison, github.com/richmorrison/cronbak",
        allow_abbrev=False
    )

    parser.add_argument(
        'src',
        type=pathlib.Path,
        help='Path to file/directory to be backed-up'
    )
    
    parser.add_argument(
        'dest',
        type=pathlib.Path,
        help='Destination location of generated archive'
    )
    
    parser.add_argument(
        '-p',
        '--prefix',
        default=None,
        help='Prefix to prepend to archive filename. Useful for identifying backup jobs (eg. weekly, monthly etc)'
    )
    
    parser.add_argument(
        '-r',
        '--retention',
        type=int,
        default=None,
        help='Maximum number of archives with PREFIX (if given) to retain. If no prefix specified, then the maximum number of archives to retain that do not have a file prefix. Oldest archives are deleted, thereby leaving RETENTION archives remaining. WARNING: This option is data destructive. USE WITH CAUTION.'
    )

    return parser

if __name__ == "__main__":
    
    args = build_parser().parse_args()
    
    run_backup(args.src.as_posix(), args.dest.as_posix(), args.prefix, args.retention)
