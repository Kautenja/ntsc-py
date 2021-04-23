
# compile the project and run the demo code
all: compile run

# compile the demo code
compile: *.c
	g++ -o demo demo.c sms_ntsc.c `sdl-config --cflags --libs`

# run the demo code
run:
	./demo
