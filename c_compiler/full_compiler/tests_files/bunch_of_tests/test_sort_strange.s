.text
.data
.LC0:
    .string "Swapping %p and %p\n"
.LC1:
    .string "Swapping %d and %d\n"
.LC2:
    .string "Addresses: %p and %p\n"
.LC3:
    .string "After swap: "
.LC4:
    .string "%d "
.LC5:
    .string "\n"
.LC6:
    .string "Tableau original: "
.LC7:
    .string "Tableau tri\xc3\xa9: "
.text
.globl swap
.globl loopedBubbleSort
.globl printArray
.globl main
swap:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	pushq -16(%rbp)
	pushq -8(%rbp)
	lea .LC0(%rip), %rax
	movq %rax, %rdi
	popq %rsi
	popq %rdx
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	movq -8(%rbp), %rax
	movq (%rax), %rax
	movq %rax, -24(%rbp)
	movq -16(%rbp), %rax
	movq (%rax), %rax
	movq -8(%rbp), %rbx
	movq %rax, (%rbx)
	movq -16(%rbp), %rbx
	movq -24(%rbp), %rax
	movq %rax, (%rbx)
	leave
	ret
loopedBubbleSort:
	pushq %rbp
	movq %rsp, %rbp
	subq $40, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	movq $0, -24(%rbp)
	.LloopedBubbleSort0H0:
	movq -16(%rbp), %rbx
	movq -24(%rbp), %rax
	cmpq %rbx, %rax
	setl %al
	movzbq %al, %rax

		cmpq $0, %rax
	je .LloopedBubbleSort1H0
	movq $0, -32(%rbp)
	.LloopedBubbleSort0H1:
	movq -16(%rbp), %rbx
	movq -32(%rbp), %rax
	cmpq %rbx, %rax
	setl %al
	movzbq %al, %rax

		cmpq $0, %rax
	je .LloopedBubbleSort1H1
	movq -32(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq (%rax), %rax
	pushq %rax
	movq -24(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq (%rax), %rax
	movq %rax, %rbx
	popq %rax
	cmpq %rbx, %rax
	setg %al
	movzbq %al, %rax

	cmpq $0, %rax
	je .LloopedBubbleSort0H2FIN0
	movq -24(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq (%rax), %rax
	pushq %rax
	movq -32(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq (%rax), %rax
	pushq %rax
	lea .LC1(%rip), %rax
	movq %rax, %rdi
	popq %rsi
	popq %rdx
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	movq -24(%rbp), %rbx
	movq -8(%rbp), %rax
	leaq (%rax, %rbx, 8), %rax
	pushq %rax
	movq -32(%rbp), %rbx
	movq -8(%rbp), %rax
	leaq (%rax, %rbx, 8), %rax
	pushq %rax
	lea .LC2(%rip), %rax
	movq %rax, %rdi
	popq %rsi
	popq %rdx
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	movq -24(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	pushq %rax
	movq -32(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq %rax, %rdi
	popq %rsi
	call swap

	lea .LC3(%rip), %rax
	movq %rax, %rdi
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	movq -8(%rbp), %rdi
	movq -16(%rbp), %rsi
	call printArray

	.LloopedBubbleSort0H2FIN0:
	.LloopedBubbleSort0H1INC:
	movq -32(%rbp), %rax
	pushq %rax
	incq %rax
	movq %rax, -32(%rbp)
	popq %rax
	jmp .LloopedBubbleSort0H1
	.LloopedBubbleSort1H1:
	.LloopedBubbleSort0H0INC:
	movq -24(%rbp), %rax
	pushq %rax
	incq %rax
	movq %rax, -24(%rbp)
	popq %rax
	jmp .LloopedBubbleSort0H0
	.LloopedBubbleSort1H0:
	leave
	ret
printArray:
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	movq $0, -24(%rbp)
	.LprintArray0H0:
	movq -16(%rbp), %rbx
	movq -24(%rbp), %rax
	cmpq %rbx, %rax
	setl %al
	movzbq %al, %rax

		cmpq $0, %rax
	je .LprintArray1H0
	movq -24(%rbp), %rbx
	movq -8(%rbp), %rax
	imulq $8, %rbx
	addq %rbx, %rax
	movq (%rax), %rax
	pushq %rax
	lea .LC4(%rip), %rax
	movq %rax, %rdi
	popq %rsi
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	.LprintArray0H0INC:
	movq -24(%rbp), %rax
	pushq %rax
	incq %rax
	movq %rax, -24(%rbp)
	popq %rax
	jmp .LprintArray0H0
	.LprintArray1H0:
	lea .LC5(%rip), %rax
	movq %rax, %rdi
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	leave
	ret
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $56, %rsp
	movq $2, %rax
	movq %rax, -8(%rbp)
	movq $6, %rax
	movq %rax, -16(%rbp)
	movq $8, %rax
	movq %rax, -24(%rbp)
	movq $3, %rax
	movq %rax, -32(%rbp)
	movq $5, %rax
	movq %rax, -40(%rbp)

	movq $8, %rbx
	movq $40, %rax
	cqto
	idivq %rbx
	movq %rax, -48(%rbp)
	lea .LC6(%rip), %rax
	movq %rax, %rdi
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	pushq -48(%rbp)
	lea -40(%rbp), %rax
	movq %rax, %rdi
	popq %rsi
	call printArray

	pushq -48(%rbp)
	lea -40(%rbp), %rax
	movq %rax, %rdi
	popq %rsi
	call loopedBubbleSort

	lea .LC7(%rip), %rax
	movq %rax, %rdi
	pushq %rbp
	movq %rsp, %rbp
	andq $-16, %rsp
	call printf
	movq %rbp, %rsp
	popq %rbp
	pushq -48(%rbp)
	lea -40(%rbp), %rax
	movq %rax, %rdi
	popq %rsi
	call printArray

	movq $0, %rax
	leave
	ret
	leave
	ret
.section .note.GNU-stack,"",@progbits
