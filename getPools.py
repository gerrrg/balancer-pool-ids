# python basics
import os
import sys
import json

# balpy subgraph module
import balpy.graph.graph as balGraph

def main():
	
	batch_size = 30;
	networks = ["mainnet", "kovan", "polygon", "arbitrum"];

	poolsPath = "./pools/";
	
	for network in networks:

		print();

		# initialize subgraph
		bg = balGraph.TheGraph(network);
		try:
			# query subgraph
			pools = bg.getV2PoolIDs(batch_size);
			
			# only save this data if there is no file, or if the new data has more pools than the old data
			poolFilePath = poolsPath + network + ".json";
			saveData = False;
			if os.path.isfile(poolFilePath):
				with open(poolFilePath, 'r') as f:
					oldPools = json.load(f);
					if oldPools["header"]["numPools"] < pools["header"]["numPools"]:
						saveData = True;
			else:
				saveData = True;

			# save data to file, nicely formatted with indents
			if saveData:
				print("Saving", network, "data to", poolFilePath);
				with open(poolFilePath, 'w') as f:
					json.dump(pools, f, indent=4);
			else:
				print("No new pools, skipping", network);
		
		# catch errors if subgraph is down or internet connection bad
		except:
			print("Unexpected error:", sys.exc_info()[0]);
	print();
	
if __name__ == '__main__':
	main();
