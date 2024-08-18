# FileExtension
## Stworzenie pełnej ścieżki

```python
from fileextend import mkdir_full

mkdir_full('a/b/c/d/e')
```

## Pobranie liczby znaków z pliku
Umożliwia także wyliczanie liczby znaków dla dużyc plików za pomocą chunków
> Drugi parametr określa rozmar chunka w MB, domyślnie 5MB

```python
from fileextend import file_get_length

print(file_get_length('/file/path.txt', 50))
```

## Wyliczenia hash sha256 dla pliku
> Drugi parametr określa rozmar chunka w MB, domyślnie 5MB

```python
from fileextend import file_get_sha256

print(file_get_sha256('/file/path.txt'))
```