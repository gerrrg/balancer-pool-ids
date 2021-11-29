import json
import os 

poolPath = "./pools"
networks = ["kovan", "mainnet", "polygon", "arbitrum"];

networksIds = {}
for network in networks:
	
	networkPools = os.path.join(poolPath, network + ".json");
	data = None;
	with open(networkPools) as f:
		data = json.load(f)

	networkIds = [];
	for poolType in data["pools"]:
		networkIds.extend(data["pools"][poolType]);

	networksIds[network] = networkIds;

for i in range(len(networks) - 1):
	currNetwork = networks[i];
	for j in range(i + 1, len(networks)):
		nextNetwork = networks[j];
		overlap = list(set(networksIds[currNetwork]) & set(networksIds[nextNetwork]))

		if len(overlap) > 0:
			print("Found", len(overlap), "collisions between", currNetwork, "and", nextNetwork);
			print("\t",overlap)
		else:
			print("Found no collisions between", currNetwork, "and", nextNetwork);

