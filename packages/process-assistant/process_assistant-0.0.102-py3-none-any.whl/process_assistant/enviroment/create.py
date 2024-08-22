'''Este paquete esta dedicado a crear un entorno virtial para el proyecto'''
#!/usr/bin/env python3

import subprocess

from .import command

def create_virtualenv():
  ps = subprocess.run(command.CREATE_VIRTUALENV, shell=True, capture_output=True, text=True)
  print(ps.stdout)
  print(ps.stderr)

def exist_virtualenv():
  ps = subprocess.run(command.EXIST_CREATE_VIRTUALENV, shell=True, capture_output=True, text=True)
  print(ps.stdout)
  print(ps.stderr)
  print(ps.returncode)