Gnome Quota Indicator
---------------------
This is a small app which shows the current quota usage of the logged on user as well as some stats of specified filesystems.

NOTE: only python3 and GTK 3.0+ is supported

### Config
```sh
---
# use filesystems in /etc/exports
use_etc_exports: True|False

# This will do df and grep for the specified filesystems
fs:
  - /ashscr1
  - /ashscr2

# when should the icon change color?
  notify_levels:
    warning: 0.8
    critical: 0.9
```

### Technology Stack
 - python3
 - Gtk 3.0

### Depenedencies
```sh
$ aptitude install python3-yaml python3-pil
```

License
-------
>Copyright (c) 2016 Anastassios Martakos
>
>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
