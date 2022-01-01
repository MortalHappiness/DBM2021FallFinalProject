.PHONY: all clean run
all: # The default target

# tool macros
CXXFLAGS := -Wall -O2 -std=c++17

# compile macros
TARGET := main

# phony rules
all: $(TARGET)

clean:
	rm -rf core.* *.o $(TARGET)

run: $(TARGET)
	@./$(TARGET)
