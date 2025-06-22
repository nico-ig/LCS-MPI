#include <mpi.h>
#include "Grid.hpp"
#include "DebugHooks.hpp"
#include "FileHandler.hpp"
#include "CommandLineParser.hpp"
#include "MemoryHandler.hpp"

int main(int argc, char** argv) {
  // Create a scope so we can clean up the memory only after the grid is destroyed
  {
    CommandLineParser parser(argc, argv);

    if (parser.helpRequested()) {
      parser.showHelp();
      return 0;
    }

    auto files = parser.getInputFiles();

    ut::utype num_threads = parser.getNumThreads();
    ut::utype block_multiplier = parser.getBlockMultiplier();

    ut::string hSeq = FileHandler::readFile(files[0]);
    ut::string vSeq = FileHandler::readFile(files[1]);
 
  
    Grid grid(hSeq, vSeq, MemoryHandler::CACHE_LINE_SIZE * block_multiplier);
    MPI_Init(&argc, &argv);
    ProcessorHook::processGridByBlock(num_threads, &grid);
    MPI_Finalize();
    MemoryHandler::freeMemory(hSeq.data());
    MemoryHandler::freeMemory(vSeq.data());
  }

  MemoryHandler::cleanup();
  return 0;
}
