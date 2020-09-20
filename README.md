# Assembly Debuger

This repo is simple `Assembly Debuger` for debuging `.asm` files using `gdb` <a href='https://sourceware.org/gdb/current/onlinedocs/gdb/Basic-Python.html'> Api </a> in python. <br />

## start

Steps of debuging file:

- put all your assembly files in `project_dir/src/asm_src`.
- put your inputs in `input.txt` file which is in root location of the project.
- then run below instructions

```bash
    cd (project folder)
    ./install.sh
```
- `please note` that every `.asm` file has main label type each of them correctly.

## Issues

if you have any problem with script please contact me any of this methods:

- emailAddress: `shafiee.mohamin@gmail.com`
- <a href='https://github.com/shamohamin/Assembly-Debuger/issues'> Issues</a>

## example

I provided some `.asm` files which you can test the app. <br/>

steps:

- run `./install.sh`
- enter labels: `asm_main,merge`
