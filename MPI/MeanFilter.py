from PIL import Image
from mpi4py import MPI
import time

from main import getStartTime

image = Image.open('test.jpg')
pixels = image.load()
width, height = image.size

comm = MPI.COMM_WORLD
size = comm.Get_size()


def master(rank):
    chunk_size = (height + size - 1) // size  # Each thread will do chunk_size rows

    # 0 is master
    # Send from 1 to n - 1 the data
    for i in range(1, size):
        start = i * chunk_size
        end = min(start + chunk_size, height)
        comm.send((start, end), dest=i)

    start = 0 * chunk_size
    end = min(start + chunk_size, height)
    print("Master with rank {} makes from {} to {}".format(rank, start, end))

    for v in range(1, width):
        for u in range(1, end):
            sumR = sumG = sumB = 0
            for j in range(-1, 1 + 1):
                for i in range(-1, 1 + 1):
                    if u + j < height and v + i < width:
                        pixel = image.getpixel((v + i, u + j))
                        rr = pixel[0]
                        rg = pixel[1]
                        rb = pixel[2]
                        sumR += rr
                        sumG += rg
                        sumB += rb

            # 3x3 kernel, value for each cell is 1/9
            sumR //= 9
            sumG //= 9
            sumB //= 9
            image.putpixel((v, u), (sumR, sumG, sumB))

    # Wait for all threads to finish and gather their data
    for i in range(1, size):
        pixels_to_put = comm.recv(source=i)
        for pixel in pixels_to_put:
            image.putpixel((pixel[0], pixel[1]), (pixel[2], pixel[3], pixel[4]))

    # Save the output image
    image.save('out.jpg')
    print("Finished!")
    time_convert(time.time() - getStartTime())


def worker(rank):
    data = comm.recv(source=0)
    print("Worker with rank {} makes from {} to {}".format(rank, data[0], data[1]))

    pixels_to_put = []

    for v in range(1, width):
        for u in range(data[0], data[1]):
            sumR = sumG = sumB = 0
            for j in range(-1, 1 + 1):
                for i in range(-1, 1 + 1):
                    if u + j < height and v + i < width:
                        pixel = image.getpixel((v + i, u + j))
                        rr = pixel[0]
                        rg = pixel[1]
                        rb = pixel[2]
                        sumR += rr
                        sumG += rg
                        sumB += rb

            # 3x3 kernel, value for each cell is 1/9
            sumR //= 9
            sumG //= 9
            sumB //= 9
            pixels_to_put.append((v, u, sumR, sumG, sumB))

    comm.send(pixels_to_put, dest=0)


def time_convert(sec):
    minutes = sec // 60
    sec = sec % 60
    hours = minutes // 60
    minutes = minutes % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(minutes), sec))
