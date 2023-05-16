import odk

od = odk.ODKFetcher()
hypernym = od.get_data_by_sense_no('가지')
print(hypernym)
