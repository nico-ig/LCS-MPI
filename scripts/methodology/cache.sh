#!/bin/bash

echo "Level,Type,Size,SizeUnit,CPUs_Shared,Instances,Associativity"

# Função para contar CPUs expandindo ranges
count_cpus() {
    local list=$1
    local count=0
    IFS=',' read -ra parts <<< "$list"
    for part in "${parts[@]}"; do
        if [[ $part == *-* ]]; then
            start=${part%-*}
            end=${part#*-}
            count=$((count + end - start + 1))
        else
            count=$((count + 1))
        fi
    done
    echo $count
}

for i in /sys/devices/system/cpu/cpu0/cache/index*; do
    level=$(<"$i/level")
    type=$(<"$i/type")
    size=$(<"$i/size")  # geralmente em KB, ex: "32K"
    ways=$(<"$i/ways_of_associativity")
    shared_cpu_map=$(<"$i/shared_cpu_list")

    # Contar número de CPUs compartilhando esse cache corretamente
    instances=$(count_cpus "$shared_cpu_map")

    # Abreviação do tipo (para referência)
    if [[ "$type" == "Data" ]]; then
        t="d"
    elif [[ "$type" == "Instruction" ]]; then
        t="i"
    else
        t="u"
    fi

    # Extrair valor numérico e unidade do tamanho
    if [[ "$size" =~ ([0-9]+)([KMG]?) ]]; then
        size_val=${BASH_REMATCH[1]}
        size_unit=${BASH_REMATCH[2]}
        [[ -z "$size_unit" ]] && size_unit="B"
    else
        size_val=$size
        size_unit="B"
    fi

    # Associatividade
    if [[ "$ways" == "0" ]]; then
        assoc="Unknown"
    elif [[ "$ways" == "255" ]]; then
        assoc="Fully associative"
    else
        assoc="${ways}-way"
    fi

    echo "L${level}${t},$type,${size_val},${size_unit},${shared_cpu_map},${instances},${assoc}"
done
