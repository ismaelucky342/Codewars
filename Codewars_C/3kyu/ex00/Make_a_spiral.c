#include <stdlib.h>
#include <string.h>

void spiralize(unsigned size, int spiral[size][size]) {
    if (size == 0) return;

    for (unsigned x = 0; x < size; x++) {
        memset(spiral[x], 0, sizeof(int) * size);
    }

    unsigned run_size = size;
    unsigned x, y, dir;
    int location[3] = {0, 0, 0};

    while (run_size >= 2 && size > 3) {
        for (x = 0; x < run_size; x++) {
            switch (location[2]) {
                case 0:
                    spiral[location[0]][location[1] + x] = 1;
                    break;
                case 1:
                    spiral[location[0] + x][location[1]] = 1;
                    break;
                case 2:
                    spiral[location[0]][location[1] - x] = 1;
                    break;
                case 3:
                    spiral[location[0] - x][location[1]] = 1;
                    break;
            }
        }


        switch (location[2]) {
            case 0:
                location[1] += x - 1;
                location[2] = 1;
                if (location[0] != 0) run_size -= 2;
                break;
            case 1:
                location[0] += x - 1;
                location[2] = 2;
                if (run_size == 2) run_size -= 1;
                break;
            case 2:
                location[1] -= x - 1;
                location[2] = 3;
                run_size -= 2;
                break;
            case 3:
                location[0] -= x - 1;
                location[2] = 0;
                if (run_size == 2) run_size -= 1;
                break;
        }
    }

    if (size <= 3) {
        memset(spiral[0], 1, sizeof(int) * size);
        if (size == 3) {
            memset(spiral[size - 1], 1, sizeof(int) * size);
        }
        for (y = 1; y < size; y++) {
            spiral[y][size - 1] = 1;
        }
    }
}
