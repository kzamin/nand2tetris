// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
    
(LOOP)
    // reset address
	@SCREEN
	D=A // D = address of screen
	@address
	M=D // M[16] = address of screen
	
	// listen to keyboard
	@KBD
	D=M // D = key pressed
	@CLEAR
	D;JEQ // if no key is pressed, move to clear
	 
(FILL)
	// set address to black
	@address
	A=M // point address to display register
	M=-1 // set word to black
	
	//incremate address
	@address
	M=M+1 
	
	// check if entire screen filled
	@24576 // highest register
	D=A 
	@address
	D=D-M // highest register minus current register
	@LOOP
	D;JLE // if hr minus cr is less than or equal to 0, goto LOOP
	@FILL
	0;JMP
	
(CLEAR)
    // set address to white
	@address
	A=M // point address to display register
	M=0 // set word to white
	
	//incremate address
	@address
	M=M+1 
	
	// check if entire screen cleared
	@24576 // highest register
	D=A 
	@address
	D=D-M // highest register minus current register
	@LOOP
	D;JLE // if hr minus cr is less than or equal to 0, goto LOOP
	@CLEAR
	0;JMP
	
	
	
	
     
     
     