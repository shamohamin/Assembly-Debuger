a.out  : io.o printArray.o merge.o main.o driver.o asm_io.o
	gcc -m32 io.o printArray.o merge.o main.o driver.o asm_io.o

io.o : io.asm
	nasm -f elf io.asm

printArray.o : printArray.asm
	nasm -f elf printArray.asm

merge.o : merge.asm
	nasm -f elf merge.asm

main.o : main.asm
	nasm -f elf main.asm

driver.o : driver.c
	gcc -m32  -c driver.c

asm_io.o : asm_io.asm
	nasm -f elf -d ELF_TYPE asm_io.asm

run: 
	./a.out < input.txt 

clean: 
	rm -rf *.out *.o 

