import odk
import graphdbGenerator

files = ['resources/1146510_150000.xml', 'resources/1146510_50000.xml', 'resources/1146510_500000.xml', 'resources/1146510_400000.xml', 'resources/1146510_800000.xml', 'resources/1146510_900000.xml', 'resources/1146510_1168166.xml', 'resources/1146510_1050000.xml', 'resources/1146510_1150000.xml', 'resources/1146510_200000.xml', 'resources/1146510_300000.xml', 'resources/1146510_750000.xml', 'resources/1146510_650000.xml', 'resources/1146510_600000.xml', 'resources/1146510_700000.xml', 'resources/1146510_350000.xml', 'resources/1146510_250000.xml', 'resources/1146510_1100000.xml', 'resources/1146510_1000000.xml', 'resources/1146510_950000.xml', 'resources/1146510_850000.xml', 'resources/1146510_450000.xml', 'resources/1146510_550000.xml', 'resources/1146510_100000.xml']

od = odk.ODKReader()
data = od.get_data_by_file_reader('resources/1146510_50000.xml')

dbGen = graphdbGenerator.GraphDBGenerator
dbGen.create_nodes_with_relations(dbGen, data)
