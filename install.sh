#!/bin/bash

echo "$OSTYPE"

RED=`tput setaf 1`
GREEN=`tput setaf 2`
NC=`tput sgr0`

src_dir='src/asm_src'


sleep_and_clear () {
    sleep $1
    clear
}

handling_errors_and_successtions () {
    if [[ $? -eq 0 ]]; then
        echo "${GREEN} ${1} was successful!${NC} $2"
    else
        echo "${RED} ${1} was not successfull!${NC} $2"4
        cleaning_source_folder
        exit 1
    fi
}

starting_make_file_sequence () {
    python3 run.py
    handling_errors_and_successtions "makeing makefile" 
}


compile_files () {
    compile_result=`make --directory=$src_dir`
    handling_errors_and_successtions "compiling" $compile_result
}

cleaning_source_folder () {
    cleaning_pattern='.(o|out)$'
    files=`ls ${src_dir}`

    for file in $files; do
        echo "$file" | grep -P -q $cleaning_pattern
        
        if [[ $? -eq 0 ]]; then
            echo "${GREEN} cleaning file: $src_dir/$file ${NC}"
            `rm -rf $src_dir/$file`
        fi
    done

    rm -rf src/temp
}

if [ "$OSTYPE" = "linux-gnu" ]; then
    # installing dependecies
    sudo apt-get update
    sudo apt-get install gdb make python3

    sleep_and_clear 1

    starting_make_file_sequence

    # compiling files 
    echo "compiling result is: "
    compile_files
    
    sleep_and_clear 2

    echo "starting execution: "
    gdb src/asm_src/a.out -q -x gdb_execution.py
    handling_errors_and_successtions "execution"
else
    echo "${RED} Your os doenst support this script. ${NC}"
fi

cleaning_source_folder