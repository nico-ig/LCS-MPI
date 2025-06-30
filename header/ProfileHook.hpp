#pragma once

#include <mpi.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>

struct MPIProfileHook {
    static std::stringstream& profile_str() {
        static std::stringstream _profile_str_instance;
        return _profile_str_instance;
    }

    static double init_time() {
        static const double _init_time = MPI_Wtime();
        return _init_time;
    }

    static inline void init() {
        MPI_Barrier(MPI_COMM_WORLD);
        profile_str() << "#RUN# start_time,end_time,elapsed_time" << std::endl;
        init_time();
    }
    static inline double getTime() {
        return MPI_Wtime();
    }
    
    static inline void addTime(double start_time, double end_time) {}

    static inline void finalize() {
        MPI_Barrier(MPI_COMM_WORLD);
        double elapsed_time = getTime() - init_time();
        profile_str() << "#RUN# " << std::fixed << std::setprecision(6)
              << init_time() << "," << getTime() << "," << elapsed_time << std::endl;
        char* filename = std::getenv("MPI_PROFILE_NAME");
        std::string filename_str = filename != nullptr ? std::string(filename) : "profile.csv";
        std::ofstream out_file(filename_str, std::ios::app);
        out_file << profile_str().str();
        out_file.close();
    }

    static inline void printLength(size_t length) {
        profile_str() << "#RUN# length=" << length << std::endl;
    }
};

struct MPIProfileSeqHook {
    static std::stringstream& profile_str() {
        return MPIProfileHook::profile_str();
    }

    static inline double init_time() {
        return MPIProfileHook::init_time();
    }
    static inline void init() {
        MPI_Barrier(MPI_COMM_WORLD);
        MPIProfileHook::profile_str() << "#PROFILE# start_time,end_time,elapsed_time" << std::endl;
        MPIProfileHook::init_time();
    }

    static inline double getTime() {
        return MPIProfileHook::getTime();
    }

    static inline void addTime(double start_time, double end_time) {
        double elapsed_time = end_time - start_time;
        MPIProfileHook::profile_str() << "#PROFILE# " << std::fixed << std::setprecision(6)
              << start_time << "," << end_time << "," << elapsed_time << std::endl;
    }

    static inline void finalize() {
        MPI_Barrier(MPI_COMM_WORLD);
        addTime(init_time(), getTime());
        char* filename = std::getenv("MPI_PROFILE_NAME");
        std::string filename_str = filename != nullptr ? std::string(filename) : "profile_seq.csv";
        std::ofstream out_file(filename_str, std::ios::app);
        out_file << profile_str().str();
        out_file.close();
    }

    static inline void printLength(size_t) {
    }
};


#ifdef PROFILE
    using ProfileHook = MPIProfileSeqHook;
#else
    using ProfileHook = MPIProfileHook;
#endif
