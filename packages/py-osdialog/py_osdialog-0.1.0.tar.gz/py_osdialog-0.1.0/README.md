# pydialog

Python bindings for [osdialog](https://github.com/AndrewBelt/osdialog). Supports MacOS (Cocoa), Windows (WinAPI), Linux (GTK2+3 or Zenity).

## API

Message Box:
```python
# pydialog.alert(message, &optional level, button_types)

if pydialog.alert("Yes or no?", pydialog.WARNING, pydialog.YES_NO):
    print("YES!")
else:
    print("No")
```

Input Prompt:
```python
# pydialog.prompt(message, &optional default_text, level)
```

Open File Dialog:
```python
# pydialog.open_file(start_path, &optional default_text, filter)
```

Open Directory Dialog:
```python
# pydialog.open_dir(start_path, &optional default_text, filter)
```

Save File Dialog:
```python
# pydialog.save_file(start_path, &optional default_text, filter)
```

Color Picker Dialog:
```python
# pydialog.color_picker(initial_r, initial_g, initial_b, initial_a)
```

Prompt Levels:
```python
pydialog.INFO
pydialog.WARNING
pydialog.CRITICAL
```

Prompt Buttons:
```python
pydialog.OK
pydialog.OK_CANCEL
pydialog.YES_NO
```

## LICENSE
```
The MIT License (MIT)

Copyright (c) 2024 George Watson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
