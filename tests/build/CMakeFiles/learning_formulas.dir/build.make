# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/michal99/Projects/learning-formulas/tests

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/michal99/Projects/learning-formulas/tests/build

# Include any dependencies generated for this target.
include CMakeFiles/learning_formulas.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/learning_formulas.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/learning_formulas.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/learning_formulas.dir/flags.make

CMakeFiles/learning_formulas.dir/formulas.cpp.o: CMakeFiles/learning_formulas.dir/flags.make
CMakeFiles/learning_formulas.dir/formulas.cpp.o: ../formulas.cpp
CMakeFiles/learning_formulas.dir/formulas.cpp.o: CMakeFiles/learning_formulas.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/michal99/Projects/learning-formulas/tests/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/learning_formulas.dir/formulas.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/learning_formulas.dir/formulas.cpp.o -MF CMakeFiles/learning_formulas.dir/formulas.cpp.o.d -o CMakeFiles/learning_formulas.dir/formulas.cpp.o -c /home/michal99/Projects/learning-formulas/tests/formulas.cpp

CMakeFiles/learning_formulas.dir/formulas.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/learning_formulas.dir/formulas.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/michal99/Projects/learning-formulas/tests/formulas.cpp > CMakeFiles/learning_formulas.dir/formulas.cpp.i

CMakeFiles/learning_formulas.dir/formulas.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/learning_formulas.dir/formulas.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/michal99/Projects/learning-formulas/tests/formulas.cpp -o CMakeFiles/learning_formulas.dir/formulas.cpp.s

# Object files for target learning_formulas
learning_formulas_OBJECTS = \
"CMakeFiles/learning_formulas.dir/formulas.cpp.o"

# External object files for target learning_formulas
learning_formulas_EXTERNAL_OBJECTS =

learning_formulas: CMakeFiles/learning_formulas.dir/formulas.cpp.o
learning_formulas: CMakeFiles/learning_formulas.dir/build.make
learning_formulas: CMakeFiles/learning_formulas.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/michal99/Projects/learning-formulas/tests/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable learning_formulas"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/learning_formulas.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/learning_formulas.dir/build: learning_formulas
.PHONY : CMakeFiles/learning_formulas.dir/build

CMakeFiles/learning_formulas.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/learning_formulas.dir/cmake_clean.cmake
.PHONY : CMakeFiles/learning_formulas.dir/clean

CMakeFiles/learning_formulas.dir/depend:
	cd /home/michal99/Projects/learning-formulas/tests/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/michal99/Projects/learning-formulas/tests /home/michal99/Projects/learning-formulas/tests /home/michal99/Projects/learning-formulas/tests/build /home/michal99/Projects/learning-formulas/tests/build /home/michal99/Projects/learning-formulas/tests/build/CMakeFiles/learning_formulas.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/learning_formulas.dir/depend

