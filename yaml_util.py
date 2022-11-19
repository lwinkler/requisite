#! env python3

import yaml

import design_util as du
from pathlib import Path

def read_design(path: Path) -> du.Design:
	"""Read a full design document in YAML format"""
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


