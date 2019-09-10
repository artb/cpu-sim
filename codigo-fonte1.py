multi:lw $t0,operand1 
lw $t1,counter 

bz $t0,$t1,loadanswer 

lw $t0,operand2 
lw $t1,answer 
add $t1,$t0 
sw $t1,answer 
lw $t1,counter 
lw $t0,one 
add $t1,$t0 
sw $t1,counter 
lw $t0,zero 
lw $t1,zero 
bz $t0,$t1,multi 
loadanswer: lw $t0,answer 
print $t0 
stop 
.data 
operand1:.word 3 
operand2:.word 2 
counter:.word 0 
answer:.word 0 
one:.word 1 
zero:.word 0 