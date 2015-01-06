#! /usr/bin/env python

import os
import sys
import json
import shlex
import subprocess
import argparse

def sdz_url( user, password, address ):
  address='http://' + user + ':' + password + '@' + address
  return address

def process_string( input_string ):
  cmd=input_string
  print( cmd )
  args=shlex.split(cmd)
  val=subprocess.Popen(args)
  val.wait()

def update_project( remote, branches ):
  process_string( 'git fetch ' + remote )
  process_string( 'git fetch ' + remote + ' --tags' )
  process_string( 'git push sdz --tags' )

  process_string( 'git fetch ' + remote )

  for b in branches:
    process_string( 'git checkout -t ' + remote + '/' + b )
    process_string( 'git checkout ' + b )
    process_string( 'git pull ' + remote + ' ' + b )
    process_string( 'git push sdz ' + b )

if __name__ == "__main__":
  parser=argparse.ArgumentParser()
  parser.add_argument( "--json", help="input json file" )
  parser.add_argument( '-o', "--output", help="output directory")
  parser.add_argument( '-u', "--user", help="user name" )
  parser.add_argument( '-p', "--password", help="password" )
  args = parser.parse_args()

  filename=args.json
  output=args.output
  user=args.user
  password=args.password

  wrongargs=False

  if filename is None:
    wrongargs=True

  if output is None:
    wrongargs=True

  if user is None:
    wrongargs=True

  if password is None:
    wrongargs=True

  if wrongargs:
    parser.print_help()
    sys.exit(1)

  json_file=open( filename )
  json_data=json.load( json_file )

  projects=json_data["projects"]

  os.chdir( output )
  print( 'number of projects: ' + str( len( projects) ) )

  for p in projects:
    name = p["name"]
    print( '* update ' + name )
    repositories=p["repositories"]

    if os.path.isdir( os.path.join( output, name ) ):
      if os.path.isdir( os.path.join( output, name, '.git' )):
        os.chdir( os.path.join( output, name ) )
        for r in repositories:
          update_project( r["remote"], r["branches"] )
      else:
        print( 'directory exists but not a git repository' )
        sys.exit(1)
    else:
      os.chdir( output )

      git_clone_cmd='git clone -o ' + repositories[0]["remote"] + ' ' + repositories[0]["url"] + ' ' + name
      process_string( git_clone_cmd )

      os.chdir( os.path.join( output, name ) )

      git_remote_add_sdz_cmd='git remote add sdz ' + sdz_url( user, password, p["sdz"] )
      process_string( git_remote_add_sdz_cmd )

      for r in repositories:
        if r is not repositories[0]:
          process_string( 'git remote add ' + r["remote"] + ' ' + r["url"] )
        update_project( r["remote"], r["branches"] )

  json_file.close()
