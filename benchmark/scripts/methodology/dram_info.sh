#!/bin/bash

echo "Locator,Size,Speed,Type,FormFactor,Manufacturer,PartNumber"

sudo dmidecode -t 17 | awk -F: '
BEGIN {OFS=","}
/Locator:/ && !/Bank Locator/ {loc=$2; gsub(/^[ \t]+|[ \t]+$/, "", loc)}
/^\t*Size:/ {size=$2; gsub(/^[ \t]+|[ \t]+$/, "", size);}
/Type:/ && !/Detail/ {type=$2; gsub(/^[ \t]+|[ \t]+$/, "", type)}
/Form Factor:/ {form=$2; gsub(/^[ \t]+|[ \t]+$/, "", form)}
/Speed:/ && /MT\/s/ {speed=$2; gsub(/^[ \t]+|[ \t]+$/, "", speed)}
/Manufacturer:/ {manu=$2; gsub(/^[ \t]+|[ \t]+$/, "", manu)}
/Part Number:/ {part=$2; gsub(/^[ \t]+|[ \t]+$/, "", part)}
/^$/ {
    if (size != "" && size != "No Module Installed" && size != "None" && loc != "") {
        print loc, size, speed, type, form, manu, part
    }
    loc=size=speed=type=form=manu=part=""
}'
