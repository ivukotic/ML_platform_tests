apt-get update -y
apt-get install -y ninja-build libprotobuf-dev protobuf-compiler python3-pip
pip3 install meson
apt-get install -y clang-6.0

echo "Installing lc0"
rm -rf lc0 
git clone --recurse-submodules https://github.com/LeelaChessZero/lc0.git
cd lc0 && git checkout $(git tag --list |grep -v rc |tail -1)
CC=clang-6.0 CXX=clang++-6.0 ./build.sh
mv ./build/release/lc0 lc0

echo "Downloading lczero client"
curl -s -L https://github.com/LeelaChessZero/lczero-client/releases/latest | egrep -o '/LeelaChessZero/lczero-client/releases/download/.*/lc0-training-client-linux' | head -n 1 | wget --base=https://github.com/ -i - -O client_linux && chmod +x client_linux

echo "Running Leela Chess Zero"
./client_linux --user googlecloud --password googlecloud