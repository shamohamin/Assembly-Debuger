%include "asm_io.inc"

segment .text
    global printArray

printArray:
    push ebp 
    mov ebp , esp

    push edx
    push ecx 
    mov edx , [ebp + 8] ;have address of label
    mov ecx , 0

print_for:

    mov eax , [edx + ecx]
    cmp eax , 0
    je end_print_loop
    add ecx , 4
    call print_int
    mov al , 32
    call print_char 
    jmp print_for

end_print_loop:
        
    pop ecx
    pop edx
    pop ebp
    ret