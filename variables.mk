HEADER_DIR = header
SRC_DIR = src
BUILD_DIR = build

TARGET ?= lcs

CXX = mpic++
CFLAGS = -std=c++17
LDFLAGS =

RELEASE_CFLAGS = -O3 -march=native
DEBUG_CFLAGS = -fno-omit-frame-pointer -O0 -g

WARNINGS = -Wall -Wextra -Wshadow -Wconversion -Wpedantic -Wsign-compare -Wconversion \
					 -Wunused -Wunused-parameter -Wunused-variable -Wunused-function \
					 -Wunused-but-set-variable -Wunused-but-set-parameter -Wunused-result

REMOTE_DIR = LCS-MPI
REMOTE_HOST = localhost
HOSTFILE = hostfile.txt
NUMPROCESS = 2
RUN_SCRIPT = ./benchmark/scripts/utils/run-mpi.sh ./
