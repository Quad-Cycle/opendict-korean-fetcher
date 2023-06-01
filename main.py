import odk
import graphDBGenerator
import glob

od = odk.ODKReader()
dbGen = graphDBGenerator.GraphDBGenerator()

# generate neo4j db
# for filePath in glob.glob('resources/*.xml'):
#     data = od.get_data_by_file_reader(filePath)
#     dbGen.create_nodes_with_relations(data)

# search word
dbGen.search_HYPERNYM(['경북', '경남'])
