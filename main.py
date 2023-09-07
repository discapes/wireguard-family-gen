#!/bin/python

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import qrcode
import shutil

main_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
out_dir = main_dir + "scripts/"
env = Environment(
	loader=FileSystemLoader(main_dir),
	trim_blocks = True
	)
template = env.get_template("script.sh.j2")
client_conf_template = env.get_template("wg0.conf.client.j2")
hosts_template = env.get_template("hosts.j2")

shutil.rmtree(out_dir, ignore_errors=True)
os.mkdir(out_dir)

with open("config.yml", "r") as file:
	yml = yaml.safe_load(file)

	with open(out_dir + yml["server"]["filename"] + ".sh", "w") as fh:
		rendered = template.render(yml["server"] | {"clients": yml["clients"], "is_server": True})
		fh.write(rendered)

	with open(main_dir + "ansible/hosts", "w") as fh:
		rendered = hosts_template.render(yml)
		fh.write(rendered)

	for client in yml["clients"]:
		context = client | {"server": yml["server"]}
		if "qrcode" in client:
			rendered_conf = client_conf_template.render(context)
			qrcode.make(rendered_conf).save(out_dir + client["filename"] + ".png")
		elif "configonly" in client:
			with open(out_dir + client["filename"] + ".conf", "w") as fh:
				rendered = client_conf_template.render(context)
				fh.write(rendered)
		else:
			with open(out_dir + client["filename"] + ".sh", "w") as fh:
				rendered = template.render(context)
				fh.write(rendered)