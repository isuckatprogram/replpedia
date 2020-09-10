import database

def search(value):
  results = database.get_wikis({})
  results_array = []
  for i in results:
    if i['name'].find(value) != -1:
      i.pop('_id')
      results_array.append(i)
    elif i['content'].find(value) != -1:
      i.pop('_id')
      results_array.append(i)
    elif i['author'].find(value) != -1:
      i.pop('_id')
      results_array.append(i)
    print(results_array)
  return results_array