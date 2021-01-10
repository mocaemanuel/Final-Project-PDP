from mpi4py import MPI
import time
import MeanFilter

comm = MPI.COMM_WORLD
size = comm.Get_size()
print('size = ', size)
current_time = time.time()


def main():
    rank = comm.Get_rank()
    if rank == 0:
        MeanFilter.master(rank)
    else:
        MeanFilter.worker(rank)


def getStartTime():
    return current_time


if __name__ == '__main__':
    current_time = time.time()
    main()
