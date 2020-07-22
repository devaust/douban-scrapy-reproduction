import pandas as pd

data = pd.read_csv('./user_seen_movie_merged.csv')
result = pd.DataFrame(columns = ['user_id', 'movie_id'])
#data = pd.read_csv("/Users/macbook/Downloads/user_seen_movie_merged.csv")
for i in range(1308):
    o = data['movie_id'][i].split('/', -1)
    o = list(set((o)))
    print(o)
    o = '/'.join(o)
    result.loc[i] = [data['user_id'][i], o]

print(result)
result.to_csv('out_put.csv', index = False)
