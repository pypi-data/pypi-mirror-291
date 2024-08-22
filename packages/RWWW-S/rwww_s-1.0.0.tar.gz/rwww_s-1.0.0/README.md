This is a tool for removing www. and https://www. in dictionary's. It was created partially by the tabnine ai and Me. Note that it creates a new dictionary and the original one is unchanged.

<h4>Example of how it works</h4>

```python
from RWs import remove_www_fKey, remove_www_fVal, remove_www

example_dict = {
    "www.example": "https://www.example.com"
}

example_dict_2 = remove_www_fKey(example_dict)
print(example_dict_2)

example_dict_cop = remove_www_fVal(example_dict)
print(example_dict_cop)

example_dict_co = remove_www(example_dict)
print(example_dict_co)
```

<h4>Result</h4>

```py
{'example': 'https://www.example.com'}
{'www.example': 'example.com'}
{'example': 'example.com'}
```

<h4>How to download</h4>

```py
pip install RWW_S
```
