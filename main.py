#!/bin/python

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil

main_dir = os.path.dirname(os.path.realpath(__file__))
out_dir = main_dir + "/scripts/"
env = Environment(
	loader=FileSystemLoader(main_dir),
	trim_blocks = True
	)
server_tmp = env.get_template("server.j2")
client_tmp = env.get_template("client.j2")

shutil.rmtree(out_dir, ignore_errors=True)
os.mkdir(out_dir)

with open("config.yml", "r") as file:
	yml = yaml.safe_load(file)

	with open(out_dir + yml["server"]["filename"] + ".sh", "w") as fh:
		rendered = server_tmp.render(**yml)
		fh.write(rendered)

	for client in yml["clients"]:
		with open(out_dir + client["filename"] + ".sh", "w") as fh:
			rendered = client_tmp.render(client=client, server=yml["server"])
			fh.write(rendered)