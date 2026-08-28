from retrieve_data import retrieve_data

print("--------- Test 1: Only date ---------")
df = retrieve_data(date=['2019-01-01', '2019-01-31'])
print(df.shape)
print(df.head())

print("\n--------- Test 2: Only products ---------")
df = retrieve_data(product_code=18)
print(df.shape)
print(df.head())

print("\n--------- Test 3: Only store ---------")
df = retrieve_data(store_code=1)
print(df.shape)
print(df.head())

print("\n---------Test 4: All filters ---------")
df = retrieve_data(product_code=18, store_code=1, date=['2019-01-01', '2019-01-31'])
print(df.shape)
print(df.head())

print("\n--------- Test 5: No filters ---------")
df = retrieve_data()
print(df.shape)