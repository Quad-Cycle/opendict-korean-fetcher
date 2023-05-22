import math
import time
import odk
import graphdbGenerator
import glob

od = odk.ODKReader()
dbGen = graphdbGenerator.GraphDBGenerator()

# generate neo4j db
for filePath in glob.glob('resources/*.xml'):
    data = od.get_data_by_file_reader(filePath)
    dbGen.create_nodes_with_relations(data)

# search word
# start = time.time()
# dbGen.search_HYPERNYM('고양이')
# end = time.time()

# print(f"{end - start:.5f} sec")
