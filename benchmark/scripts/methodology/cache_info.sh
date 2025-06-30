#!/bin/bash

# Get lscpu cache information
# Parse cache information from lscpu
lscpu_cache=$(lscpu | awk '
/L[123][di]? cache:/ {
    # Extract level (L1d, L1i, L2, L3)
    level = $1
    # Get size (including unit)
    size = $3 " " $4
    # Get instances count (remove parentheses)
    gsub(/[()]/, "", $5)
    instances = $5
    
    # Store in variables based on level
    if (level == "L1d") { l1d_size = size; l1d_inst = instances }
    if (level == "L1i") { l1i_size = size; l1i_inst = instances }
    if (level == "L2")  { l2_size = size; l2_inst = instances }
    if (level == "L3")  { l3_size = size; l3_inst = instances }
}
END {
    print l1d_size, l1d_inst, l1i_size, l1i_inst, l2_size, l2_inst, l3_size, l3_inst
}')

# Read lscpu cache info into variables
read l1d_size l1d_unit l1d_instances \
     l1i_size l1i_unit l1i_instances \
     l2_size l2_unit l2_instances \
     l3_size l3_unit l3_instances <<< "$lscpu_cache"

# Process cpuid output to get associativity
cpuid -1 | awk -v l1d_inst="$l1d_instances" \
               -v l1i_inst="$l1i_instances" \
               -v l2_inst="$l2_instances" \
               -v l3_inst="$l3_instances" \
               -v l1d_size="$l1d_size" \
               -v l1i_size="$l1i_size" \
               -v l2_size="$l2_size" \
               -v l3_size="$l3_size" \
               -v l1d_unit="$l1d_unit" \
               -v l1i_unit="$l1i_unit" \
               -v l2_unit="$l2_unit" \
               -v l3_unit="$l3_unit" '
BEGIN {
    FS = OFS = ","
    print "Level,Size,Unit,Instances,Associativity"
}
/^ *L[123].*(data|instruction|unified)?.*cache information/ && !/TLB/ {
    # Print previous cache if we have one
    if (level != "") {
        print_cache()
    }

    # Extract level (L1/L2/L3)
    level = ($1 ~ /L1/) ? "L1" : ($1 ~ /L2/) ? "L2" : "L3"

    if ($0 ~ /data/) type = "d"
    else if ($0 ~ /instruction/) type = "i"
    else type = ""

    # Reset metrics
    assoc = "N/A"
}
/^ *associativity/ {
    if (match($0, /\(([0-9]+)\)/, arr)) {
        assoc = arr[1] == "255" ? "Fully associative" : arr[1] "-way"
    }
}
END {
    # Print the last cache if we have one
    if (level != "") {
        print_cache()
    }
}
function print_cache() {
    if (level == "L1" && type == "d") {
        print "L1d", l1d_size, l1d_unit, l1d_inst, assoc
    }
    else if (level == "L1" && type == "i") {
        print "L1i", l1i_size, l1i_unit, l1i_inst, assoc
    }
    else if (level == "L2") {
        print "L2", l2_size, l2_unit, l2_inst, assoc
    }
    else if (level == "L3") {
        print "L3", l3_size, l3_unit, l3_inst, assoc
    }
}'
