#! env python3

import yaml

from classes import *
from pathlib import Path

def read_design(path: Path) -> Design:
	with open(path) as fin:
		return yaml.safe_load(fin.read())
	

# garage1 = Garage("mygarage", [
	# Vehicle('spam1', 'eggs'),
	# Vehicle('spam2', 'eggs'),
	# Vehicle('adfasdf', 'eggs'),
	# Vehicle('spam', 'eggs'),
	# Vehicle('spam', 'eggs'),
	# Vehicle('AAA', 'eggs')
	# ])
# serialized_garage1 = yaml.dump(garage1)
# 
# with open("out.yaml", "w") as fout:
	# fout.write(serialized_garage1)
# 
# print(serialized_garage1)
# deserialized_garage1 = yaml.safe_load(serialized_garage1)
# print("name: %s, vehicles: %s" % (deserialized_garage1.name, deserialized_garage1.vehicles))


design = read_design(Path("design.yaml"))

print(design.requirements)
print(design.definitions)

print(f"Read {len(design.requirements)} requirements and {len(design.definitions)} definitions")

el = design.requirements[0]

print(el)
# print(el.to_yaml())
print(el.yaml_tag)
