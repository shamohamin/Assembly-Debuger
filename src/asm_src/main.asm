%include "asm_io.inc"

segment .bss 
    l1: resd 1000
    l2: resd 1000
    l3: resd 2000
    ;l1_size: resd 1
    ;l2_size: resd 1

segment .text
    global asm_main
    extern readArray , printArray , merge
asm_main:
    enter 0 , 0
    pusha
    
    push l1
    call readArray
    add esp , 4 
    ;mov dword [l1_size] , eax
    push l2
    call readArray
    add esp , 4
    ;mov dword [l2_size] , eax

    mov ecx , 0 ;counter for l1 which is i 
    mov ebx , 0 ;counter for l2 which is j
    mov edi , 0 ;counter for l3
    mov dword [l3] , 0

loop_for_merge:

    ;cmp dword [l1 + ecx] , 0
    ;je end_for_merge
    ;cmp dword [l2 + ebx] , 0
    ;je end_for_merge
    push ecx
    push ebx
    push edi
    push l3
    push l2
    push l1
    
    
    call merge
    add esp , 24 ;
    
    cmp eax , 1
    je l2_counter_increase
    cmp eax , 0
    jne print_array
    add ecx , 4
return_point:
    add edi , 4
    jmp loop_for_merge

l2_counter_increase:
    add ebx , 4
    jmp return_point

print_array:

    push edi
    push l3
    call printArray
    add esp , 8


    popa 
    leave 
    ret
