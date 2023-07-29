# python basics
import os
import sys
import json

# balpy subgraph module
import balpy.graph.graph as balGraph

def main():
	
	batch_size = 300;
	networks = ["mainnet", "polygon", "arbitrum", "goerli", "fantom", "optimism", "gnosis", "polygon-zk", "sepolia"];

	poolsPath = "./pools/";
	
	for network in networks:

		print(network);

		# initialize subgraph
		customEndpoint = None;
		if network == "fantom":
			customEndpoint = "https://api.thegraph.com/subgraphs/name/beethovenxfi/beethovenx"
		if network == "optimism":
			customEndpoint = "https://api.thegraph.com/subgraphs/name/beethovenxfi/beethovenx-optimism"
		if network == "gnosis":
			customEndpoint = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gnosis-chain-v2"
		if network == "sepolia":
			customEndpoint = "https://api.studio.thegraph.com/query/24660/balancer-sepolia-v2/version/latest"
		if network == "polygon-zk":
			customEndpoint = "https://api.studio.thegraph.com/query/24660/balancer-polygon-zk-v2/version/latest"
		bg = balGraph.TheGraph(network, customUrl=customEndpoint);

		# only save this data if there is no file, or if the new data has more pools than the old data
		poolFilePath = poolsPath + network + ".json";
		saveData = False;

		try:
			# query subgraph
			pools = bg.getV2PoolIDs(batch_size);
			
			if os.path.isfile(poolFilePath):
				with open(poolFilePath, 'r') as f:
					oldPools = json.load(f);
					if oldPools["header"]["numPools"] < pools["header"]["numPools"]:
						saveData = True;
			else:
				saveData = True;

		# delete empty or malformed json
		except json.decoder.JSONDecodeError:
			print("Decoder error -- deleting", poolFilePath);
			os.remove(poolFilePath);
			saveData = False;
		# catch errors if subgraph is down or internet connection bad
		except:
			print("Unexpected error:", sys.exc_info()[0]);

		# save data to file, nicely formatted with indents
		if saveData:
			print("Saving", network, "data to", poolFilePath);
			with open(poolFilePath, 'w') as f:
				json.dump(pools, f, indent=4);
		else:
			print("No new pools or query failed; skipping", network);

	print();
	
if __name__ == '__main__':
	main();
