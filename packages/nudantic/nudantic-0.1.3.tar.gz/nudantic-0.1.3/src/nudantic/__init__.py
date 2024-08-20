"""
### Nudantic
> Numpy Array type compatible with Pydantic
"""
from typing import Annotated
import numpy as np

class ArrayAnnotation:
  @classmethod
  def __get_pydantic_core_schema__(cls, *_):
    from pydantic_core.core_schema import no_info_after_validator_function, plain_serializer_function_ser_schema, any_schema
    import numpy as np
    def validate(xs: list):
      return np.array(xs)

    return no_info_after_validator_function(
      validate, any_schema(),
      serialization=plain_serializer_function_ser_schema(lambda x: x.tolist())
    ) # type: ignore
  
NdArray = Annotated[np.ndarray, ArrayAnnotation]
"""
Simple array that gets serialized to a list.


```
class MyModel(BaseModel):
  array: NdArray

MyModel(array=np.array([1, 2, 3])).model_dump_json()
# {'array': [1, 2, 3]}
```
"""