segment .data 
    l1_value: dd 0
    l2_value: dd 0

segment .text 
    global merge

merge:
    
    push ebp 
    mov ebp , esp 

    ;preserve the registers from changes
    push edx 
    push ebx 
    push ecx
    push edi 
    push esi 

    mov eax , [ebp + 20] ;is k
    mov edx , [ebp + 8] ;l1 address
    mov ebx , [ebp + 12] ;l2 address 
    mov ecx , [ebp + 16] ;l3 address
    mov edi , [ebp + 28] ;is i 
    mov esi , [ebp + 24] ;is j
    mov esi , [ebx + esi] ;have j element
    mov edi , [edx + edi] ;have i element

    cmp edi , esi ;if i element of l1 is less than j element of l2
    jle one_label

    mov edi , [ebp + 28] ; is i
    cmp esi , 0
    je else_item_from_l1   
    mov dword [ecx + eax] , esi
    add eax , 4
    mov dword [ecx + eax] , 0
    mov eax , 1
    jmp end_label

else_item_from_l1:
    mov dword [ecx + eax] , 0
    mov edx , [edx + edi]
    cmp edx , 0
    je end_label
    mov dword [ecx + eax] , edx
    add eax , 4
    add edi , 4
    mov edx , [ebp + 8] ;address of l1
    jmp else_item_from_l1
    
one_label:
    mov ecx , [ebp + 16] ; l3 address 
    mov esi , [ebp + 24] ; j element
    cmp edi , 0
    je else_item_from_l2
    mov dword [ecx + eax] , edi 
    add eax , 4
    mov dword [ecx + eax] , 0
    mov eax , 0
    jmp end_label

else_item_from_l2:
    mov dword [ecx + eax] , 0
    mov ebx , [ebx + esi] 
    cmp ebx , 0 ;l2 elements
    je end_label
    mov dword [ecx + eax] , ebx ;add to l3 
    add eax , 4
    add esi , 4
    mov ebx , [ebp + 12] ;address of l2
    jmp else_item_from_l2

end_label:

    pop esi
    pop edi
    pop ecx 
    pop ebx 
    pop edx

    pop ebp
    ret