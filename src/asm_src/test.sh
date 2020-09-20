nasm -f elf merge.asm
nasm -f elf io.asm
gcc -m32 asm_io.o merge.o io.o c.o
out=$(echo $'1 4 6 7 9 0\n2 3 8 12 23 0' | ./a.out)
res="1 2 3 4 6 7 8 9 12 23 "
echo $out
echo $res
if [ "$out" == "$res" ]; then
  echo "Success"
else
  echo "Failed"
fi