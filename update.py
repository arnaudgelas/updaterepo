#! /usr/bin/env python

import os
import sys
import json
import shlex
import subprocess

def process_string( input_string ):
  cmd=input_string
  args=shlex.split(cmd)
  val=subprocess.Popen(args)
  val.wait()

def update_project( remote, branches ):
  process_string( 'git fetch ' + remote )
  process_string( 'git fetch ' + remote + ' --tags' )

#  process_string( 'git push sdz --tags' )

  process_string( 'git fetch ' + remote )

  for b in branches:
    process_string( 'git checkout -t ' + remote + '/' + b )
    process_string( 'git pull ' + remote + ' ' + b )

#        print( 'git push sdz ' + b )
#        process_string( 'git push sdz ' + b )


filename='repositories.json'
output='/Users/arnaud/update/'
json_file=open( filename )

json_data=json.load( json_file )

projects=json_data["projects"]

print( 'number of projects: ' + str( len( projects) ) )

for p in projects:
  name = p["name"]
  print( '* update ' + name )
  repositories=p["repositories"]

  if os.path.isdir( os.path.join( output, name ) ):
    if os.path.isdir( os.path.join( output, name, '.git' )):
      for r in repositories:
        update_project( r["remote"], r["branches"] )
    else:
      print( 'directory exists but not a git repository' )
      sys.exit(1)
  else:
    print( 'git clone -o ' + repositories[0]["remote"] + ' ' + repositories[0]["url"] + ' ' + name )

    git_clone_cmd='git clone -o ' + repositories[0]["remote"] + ' ' + repositories[0]["url"] + ' ' + name
    process_string( git_clone_cmd )

    os.chdir( os.path.join( output, name ) )

#    git_remote_add_sdz_cmd='git remote add sdz ' + p["sdz"]
#    process_string( git_remote_add_sdz_cmd )

    for r in repositories:
      if r is not repositories[0]:
        process_string( 'git remote add ' + r["remote"] + ' ' + r["url"] )
      update_project( r["remote"], r["branches"] )

json_file.close()
