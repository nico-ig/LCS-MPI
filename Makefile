include variables.mk

# ======================
#  Color Definitions
# ======================
RESET   := \033[0m
BLACK   := $(RESET)\033[1;40m
GREEN   := \033[1;42m
YELLOW  := \033[1;43m
BLUE    := \033[1;44m
PURPLE  := \033[1;45m
CYAN    := \033[1;46m
WHITE   := \033[1;47m
BLACK_TEXT := \033[1;30m

# ======================
#  Logging Function
# ======================
define log
	@echo "$(BLACK_TEXT)$(1)$(2)$(RESET) $(3)"
endef

# ======================
#  Build Configuration
# ======================
BIN_DIR    := $(BUILD_DIR)/bin
OBJ_DIR    := $(BUILD_DIR)/obj

# Source files
SRC        := $(shell find $(SRC_DIR) -type f -name '*.cpp')
OBJ        := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRC))
DEP        := $(OBJ:.o=.d)

# Include paths
HEADER_PATHS := $(addprefix -I,$(shell find $(HEADER_DIR) -type d))
GENERATED_HEADERS := $(addprefix -I,$(shell find $(BUILD_DIR) -type d 2>/dev/null))

# ======================
#  Build Targets
# ======================
.PHONY: all release debug tsan clean purge help

all: release

release: CFLAGS += $(RELEASE_CFLAGS)
release: $(BIN_DIR)/$(TARGET)

profile: CFLAGS += $(DEBUG_CFLAGS) -DPROFILE
profile: clean $(BIN_DIR)/$(TARGET)

debug: CFLAGS += $(DEBUG_CFLAGS) $(WARNINGS)
debug: clean $(BIN_DIR)/$(TARGET)

# Special debug modes
debug-threads: CFLAGS += -DDEBUGTHREAD
debug-threads: debug

debug-lcs: CFLAGS += -DDEBUGLCS
debug-lcs: debug

debug-matrix: CFLAGS += -DDEBUGMATRIX
debug-matrix: debug

# Main binary target
$(BIN_DIR)/$(TARGET): $(OBJ) | $(BIN_DIR)
	$(call log,$(GREEN),Linking,$@)
	@$(CXX) $(OBJ) -o $@ $(LDFLAGS)

# Compilation rule with dependency generation
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(call log,$(YELLOW),Compiling,$<)
	@$(CXX) $(CFLAGS) -MMD -MP -c $< -o $@ $(HEADER_PATHS) $(GENERATED_HEADERS)

# Create directories
$(BIN_DIR) $(OBJ_DIR):
	@mkdir -p $@

# Include dependencies
-include $(DEP)

# ======================
#  Utility Targets
# ======================
clean:
	$(call log,$(BLUE),Cleaning,$(OBJ_DIR))
	$(call log,$(BLUE),Removing tmp dir,$(TMP_DIR))
	@rm -rf $(OBJ_DIR) vgcore* *.log $(TMP_DIR) profile.csv

purge: clean
	$(call log,$(BLUE),Removing build dir,$(BUILD_DIR))
	$(call log,$(BLUE),Removing results,$(RESULTS_DIR))
	$(call log,$(BLUE),Removing analysis dir,$(ANALYSIS_DIR))
	@rm -rf $(BUILD_DIR) $(RESULTS_DIR) $(ANALYSIS_DIR)

run:
	@$(RUN_SCRIPT)

print-binpath:
	@echo $(REMOTE_DIR)/$(BIN_DIR)/$(TARGET)

print-%:
	@echo $* = $($*)

help:
	@echo "Available targets:"
	@echo "  release       - Build optimized version (default)"
	@echo "  profile       - Build with profiling enabled"
	@echo "  debug         - Build with debug symbols and warnings"
	@echo "  run 		   - Run the application"
	@echo "  clean         - Remove build artifacts"
	@echo "  purge         - Remove all generated files"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Special debug modes:"
	@echo "  debug-threads - Enable thread debugging"
	@echo "  debug-lcs     - Enable LCS debugging"
	@echo "  debug-matrix  - Enable matrix debugging"
