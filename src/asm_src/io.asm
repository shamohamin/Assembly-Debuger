%include "asm_io.inc"

segment .text
    global readArray

readArray:

    push ebp 
    mov ebp , esp 
    push ebx
    push ecx
    push edx 
    mov ecx , 0
    mov edx , 0
    mov ebx , [ebp + 8]

input_for:

    call read_int
    cmp eax , 0
    je end_input_for
    mov dword [ebx + ecx] , eax
    add ecx , 4
    inc edx
    jmp input_for   

end_input_for:

    mov dword [ebx + ecx] , eax
    mov eax , edx

    pop edx
    pop ecx
    pop ebx
    pop ebp

    ret
