<img src="https://raw.githubusercontent.com/andrewrgarcia/rlish/main/img/rlish.svg" width="300" title="hover text">

[![License](https://img.shields.io/badge/license-%20%20GNU%20GPLv3%20-green?style=plastic)](https://raw.githubusercontent.com/andrewrgarcia/voxelmap/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/rlish/badge/?version=latest)](https://rlish.readthedocs.io/en/latest/?badge=latest)


Saving and loading information in Python should be shorter and easier.


`rlish` is a Python package for simple and efficient data serialization and deserialization. It supports both `pickle` and `joblib` serialization methods, making it suitable for a wide range of data types, including large NumPy arrays and machine learning models.


https://github.com/andrewrgarcia/rlish/assets/10375211/0bb82ada-7974-44fe-8b04-371a948285ad


## Installation

You can install `rlish` using pip:

```bash
pip install rlish
```

## Usage


### Saving Data

To save data, use the `save` function. You can choose between `pickle` and `joblib` formats:

```python
import rlish

dictionary = {'a': 1, 'b': 2, 'c': 3}
tensor = np.random.randint(0,10,(200,200,200))


# Save dictionary using pickle
rlish.save(dictionary, 'my_dictio')

# Save data using joblib
rlish.save(tensor, 'huge_tensor', format='joblib')
```

### Loading Data

To load data, use the `load` function:

```python
# Load data saved with pickle
loaded_data_pickle = rlish.load('my_dictio')

# Load data saved with joblib
loaded_data_joblib = rlish.load('huge_tensor')

# Load your data with the format printed out (if you forgot)
loaded_data_joblib = rlish.load('huge_tensor', what_is=True)
```

## Contributing

Contributions to `rlish` are welcome! Feel free to open an issue or submit a pull request.
