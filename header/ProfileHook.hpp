#pragma once

#include <mpi.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>

struct MPIProfileHook {
    static std::stringstream& profile_str(int rank) {
        static std::stringstream empty_stream;
        if (rank != 0) return empty_stream;
        static std::stringstream _profile_str_instance;
        return _profile_str_instance;
    }

    static double init_time(int rank) {
        if (rank != 0) return 0.0;
        static const double _init_time = MPI_Wtime();
        return _init_time;
    }

    static inline void init(int rank) {
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank != 0) return;
        profile_str(rank) << "#RUN# start_time,end_time,elapsed_time" << std::endl;
        init_time(rank);
    }
    static inline double getTime(int rank) {
        return MPI_Wtime();
    }
    
    static inline void addTime(double start_time, double end_time, int rank) {}

    static inline void finalize(int rank) {
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank != 0) return;
        double elapsed_time = getTime(rank) - init_time(rank);
        profile_str(rank) << "#RUN# " << std::fixed << std::setprecision(6)
              << init_time(rank) << "," << getTime(rank) << "," << elapsed_time << std::endl;
        char* filename = std::getenv("MPI_PROFILE_NAME");
        std::string filename_str = filename != nullptr ? std::string(filename) : "profile.csv";
        std::ofstream out_file(filename_str, std::ios::app);
        out_file << profile_str(rank).str();
        out_file.close();
    }

    static inline void printLength(size_t length, int rank) {
        profile_str(rank) << "#RUN# length=" << length << std::endl;
    }
};

struct MPIProfileSeqHook {
    static std::stringstream& profile_str(int rank) {
        static std::stringstream empty_stream;
        if (rank != 0) return empty_stream;
        return MPIProfileHook::profile_str(rank);
    }

    static inline double init_time(int rank) {
        if (rank != 0) return 0.0;
        return MPIProfileHook::init_time(rank);
    }
    static inline void init(int rank) {
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank != 0) return;
        MPIProfileHook::profile_str(rank) << "#PROFILE# start_time,end_time,elapsed_time" << std::endl;
        MPIProfileHook::init_time(rank);
    }

    static inline double getTime(int rank) {
        return MPIProfileHook::getTime(rank);
    }

    static inline void addTime(double start_time, double end_time, int rank) {
        if (rank != 0) return;
        double elapsed_time = end_time - start_time;
        MPIProfileHook::profile_str(rank) << "#PROFILE# " << std::fixed << std::setprecision(6)
              << start_time << "," << end_time << "," << elapsed_time << std::endl;
    }

    static inline void finalize(int rank) {
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank != 0) return;
        addTime(init_time(rank), getTime(rank), rank);
        char* filename = std::getenv("MPI_PROFILE_NAME");
        std::string filename_str = filename != nullptr ? std::string(filename) : "profile_seq.csv";
        std::ofstream out_file(filename_str, std::ios::app);
        out_file << profile_str(rank).str();
        out_file.close();
    }

    static inline void printLength(size_t, int) {
    }
};


#ifdef PROFILE
    using ProfileHook = MPIProfileSeqHook;
#else
    using ProfileHook = MPIProfileHook;
#endif
