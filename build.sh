cd core

echo "Removing previous build directory..."
rm -r build 

echo "Building code..."
mkdir -p build && cd build
cmake .. && make