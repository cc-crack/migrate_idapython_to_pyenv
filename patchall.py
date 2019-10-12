#!/usr/bin/env python
import os
import re
import argparse

patchlist = [
    {
        'path' : r'/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/plugins',
        'patt' : r'^python.*\.dylib$'
    },
    {
        'path' : r'/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python/lib/python2.7/lib-dynload/ida_32',
        'patt' : r'.+so'
    },
    {
        'path' : r'/Applications/IDA Pro 7.0/ida.app/Contents/MacOS/python/lib/python2.7/lib-dynload/ida_64',
        'patt' : r'.+so'
    }
]

def patch(oldlib,newlib,filename):
    cmd = r"install_name_tool  -change '%s' '%s' '%s' " % (oldlib,newlib,filename)
    print(cmd)
    os.system(cmd)

def patchdir(dname,fnamere,oldlib,newlib):
    g = os.walk(dname)  
    for path,dir_list,file_list in g:  
        for file_name in file_list:
            if re.match(fnamere,file_name):
                patch(oldlib,newlib,os.path.join(path, file_name))

"""
    oldlib = r'/System/Library/Frameworks/Python.framework/Versions/2.7/Python'
    newlib = r'/Users/charles/.pyenv/versions/idapython/lib/python2.7.dylib'
"""

def main():
    parser = argparse.ArgumentParser(description="IDA pro python env patcher.")
    parser.add_argument('-o', "--old-lib", type=str, help="Old Path to the python.dylib",default=r'/System/Library/Frameworks/Python.framework/Versions/2.7/Python')
    parser.add_argument('-n', "--new-lib" ,type=str, help="New Path to the python.dylib")
    args = parser.parse_args()
    if args.new_lib:
        print('Patch IDApython env from %s to %s ' % (args.old_lib,args.new_lib))
        for i in patchlist:
            patchdir(i['path'],i['patt'],args.old_lib,args.new_lib)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()