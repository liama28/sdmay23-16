# List of source files
SRCS = main.py notify.py results.py Source.c model_helper.sh ssh_helper.sh

# List of object files
OBJS = $(SRCS:.c=.o)

# Compiler flags
CFLAGS = -Wall -Werror

# Dependency flags
DEPS = ipaddr.cfg

# Name of the executable
EXEC = myprogram

# Rules
all: $(EXEC)

$(EXEC): $(OBJS) $(DEPS)
    # Command to link the object files
    @echo "Linking..."
    @echo "Command: gcc $(OBJS) -o $(EXEC)"
    gcc $(OBJS) -o $(EXEC)

%.o: %.c
    # Command to compile the C files
    @echo "Compiling $<..."
    @echo "Command: gcc $(CFLAGS) -c $<"
    gcc $(CFLAGS) -c $<

clean:
    # Command to clean the object files and executable
    @echo "Cleaning..."
    @echo "Command: rm -f $(OBJS) $(EXEC)"
    rm -f $(OBJS) $(EXEC)

install:
    # Command to install any dependencies
    @echo "Installing dependencies..."
    @echo "Command: pip install -r requirements.txt"
    pip install -r requirements.txt
