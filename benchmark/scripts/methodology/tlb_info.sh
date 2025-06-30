#!/bin/bash

cpuid -1 | grep -E 'L[12] TLB|entries|associativity' | awk '
BEGIN {
    FS = OFS = ","
    print "Level,Page Size,Instruction Entries,Instruction Associativity,Data Entries,Data Associativity"
}
/L[12] TLB/ {
    # New TLB section - store previous if exists
    if (level != "") {
        data[level][page] = level OFS page OFS ientries OFS iassoc OFS dentries OFS dassoc
    }
    # Extract level (L1/L2)
    level = ($1 ~ /L1/) ? "L1" : "L2"
    # Extract page size
    page = $0
    sub(/.*information: /, "", page)
    sub(/ pages.*/, "", page)
    # Reset values
    ientries = "N/A"
    iassoc = "N/A"
    dentries = "N/A"
    dassoc = "N/A"
}
/instruction # entries/ {
    sub(/.*\(/, "", $NF)
    sub(/\).*/, "", $NF)
    ientries = $NF
}
/instruction associativity/ {
    iassoc = clean_assoc($0)
}
/data # entries/ {
    sub(/.*\(/, "", $NF)
    sub(/\).*/, "", $NF)
    dentries = $NF
}
/data associativity/ {
    dassoc = clean_assoc($0)
}
END {
    if (level != "") {
        data[level][page] = level OFS page OFS ientries OFS iassoc OFS dentries OFS dassoc
    }
    
    # Print sorted output (L1 first, then L2)
    PROCINFO["sorted_in"] = "@ind_str_asc"
    for (lvl in data) {
        for (pg in data[lvl]) {
            print data[lvl][pg]
        }
    }
}
function clean_assoc(s) {
    sub(/.*associativity[ =]+/, "", s)
    gsub(/"/, "", s)  # Remove quotes for CSV
    if (s ~ /full|0xff|255/) return "Fully associative"
    if (s ~ /off/) return "Off"
    if (s ~ /way/) return gensub(/ *\(.*/, "", "g", s)
    if (s ~ /\(/) return gensub(/ *\(.*/, "way", "g", s)
    return s
}'
