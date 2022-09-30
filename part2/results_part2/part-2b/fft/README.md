The fft benchmark does not scale to our target number of threads (3,6,12), as it only runs with
thread numbers equal to powers of two. For this reason you only need to measure single thread
performance for the fft benchmark
