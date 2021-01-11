from mpi4py import MPI
import time
import MeanFilter

comm = MPI.COMM_WORLD
size = comm.Get_size()
print('size = ', size)
currentTime = time.time()


def main():
    rank = comm.Get_rank()
    if rank == 0:
        MeanFilter.master(rank)
    else:
        MeanFilter.worker(rank)


def getStartTime():
    return currentTime


if __name__ == '__main__':
    currentTime = time.time()
    main()

# TO RUN: mpiexec -n 3 py main.py
