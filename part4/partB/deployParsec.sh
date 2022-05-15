docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:blackscholes-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2

docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:splash2x-fft-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2

docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:freqmine-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2

docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:ferret-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2

docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:canneal-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2

docker run --cpuset-cpus="0" -d --rm --name parsec \
anakli/parsec:dedup-native-reduced \
./bin/parsecmgmt -a run -p blackscholes -i native -n 2