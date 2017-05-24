import os,sys,inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("src")]
os.makedirs(cmd_folder+"data/raw/", exist_ok=True)
os.makedirs(cmd_folder+"data/inter/", exist_ok=True)
os.makedirs(cmd_folder+"data/processed/", exist_ok=True)
