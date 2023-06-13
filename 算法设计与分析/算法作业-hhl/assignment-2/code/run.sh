echo "=====================clean old files=====================\n"
rm -rf CMakeFiles cmake_install.cmake CMakeCache.txt Makefile algorithm_assignment_2 ;
echo "=====================build: cmake CMakeLists.txt && make=====================\n"
cmake CMakeLists.txt && make
echo "=====================run: ./algorithm_assignment_2=====================\n"
./algorithm_assignment_2
