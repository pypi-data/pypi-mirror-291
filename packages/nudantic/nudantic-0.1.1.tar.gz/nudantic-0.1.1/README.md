# Nudantic

> Numpy Array type compatible with Pydantic

```python
from pydanctic import BaseModel
from nudantic import NdArray

class MyModel(BaseModel):
  array: NdArray

MyModel(array=np.array([1, 2, 3])).model_dump_json()
# {'array': [1, 2, 3]}
```
