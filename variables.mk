HEADER_DIR = header
SRC_DIR = src
BUILD_DIR = build

TARGET ?= lcs

CXX = mpic++
CFLAGS = -std=c++17 -march=native
LDFLAGS =

RELEASE_CFLAGS = -O3
DEBUG_CFLAGS = -fno-omit-frame-pointer -O0 -g

WARNINGS = -Wall -Wextra -Wshadow -Wconversion -Wpedantic -Wsign-compare -Wconversion \
					 -Wunused -Wunused-parameter -Wunused-variable -Wunused-function \
					 -Wunused-but-set-variable -Wunused-but-set-parameter -Wunused-result

RUN_SCRIPT = nohup scripts/cluster/entry.py --config scripts/configs.yml > output.log 2>&1 &
#RUN_SCRIPT = scripts/cluster/entry.py --config scripts/configs.yml
RESULTS_DIR = results
ANALYSIS_DIR = analysis
TMP_DIR = tmp
