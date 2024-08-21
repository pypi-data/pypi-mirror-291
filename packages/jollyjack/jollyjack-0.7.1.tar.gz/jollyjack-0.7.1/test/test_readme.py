### Generating a sample parquet file:
# ```
import jollyjack as jj
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np

chunk_size = 3
n_row_groups = 2
n_columns = 5
n_rows = n_row_groups * chunk_size
path = "my.parquet"

data = np.random.rand(n_rows, n_columns).astype(np.float32)
pa_arrays = [pa.array(data[:, i]) for i in range(n_columns)]
schema = pa.schema([(f'column_{i}', pa.float32()) for i in range(n_columns)])
table =  pa.Table.from_arrays(pa_arrays, schema=schema)
pq.write_table(table, path, row_group_size=chunk_size, use_dictionary=False, write_statistics=True, store_schema=False, write_page_index=True)
#```

### Generating a numpy array to read into:
# ```
# Create an array of zeros
np_array = np.zeros((n_rows, n_columns), dtype='f', order='F')
# ```

### Reading entire file into numpy array:
# ```
pr = pq.ParquetReader()
pr.open(path)

row_begin = 0
row_end = 0

for rg in range(pr.metadata.num_row_groups):
    row_begin = row_end
    row_end = row_begin + pr.metadata.row_group(rg).num_rows

    # To define which subset of the numpy array we want read into,
    # we need to create a view which shares underlying memory with the target numpy array
    subset_view = np_array[row_begin:row_end, :] 
    jj.read_into_numpy (metadata = pr.metadata
                            , parquet_path = path
                            , np_array = subset_view
                            , row_group_indices = [rg]
                            , column_indices = range(pr.metadata.num_columns)
                            , pre_buffer = True)

### Generating a torch tensor to read into:
# ```
import torch
# Create a tesnsor and transpose it to get Fortran-style order
tensor = torch.zeros(n_columns, n_rows, dtype = torch.float32).transpose(0, 1)
# ```

### Reading entire file into the tensor:
# ```
pr = pq.ParquetReader()
pr.open(path)

row_begin = 0
row_end = 0

for rg in range(pr.metadata.num_row_groups):
    row_begin = row_end
    row_end = row_begin + pr.metadata.row_group(rg).num_rows

    # To define which subset of the numpy array we want read into,
    # we need to create a view which shares underlying memory with the target numpy array
    subset_view = np_array[row_begin:row_end, :] 
    jj.read_into_torch (metadata = pr.metadata
                            , parquet_path = path
                            , tensor = tensor
                            , row_group_indices = [rg]
                            , column_indices = range(pr.metadata.num_columns)
                            , pre_buffer = True)


print(np_array)
# ```
