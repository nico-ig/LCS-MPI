# Get and format CPU lists
online_cpus=$(lscpu | grep -i "on-line" | awk -F': ' '{print $2}' | xargs)
offline_cpus=$(lscpu | grep -i "off-line" | awk -F': ' '{print $2}' | xargs)

# Check if Hyper-Threading is ACTIVE
if [ -f /sys/devices/system/cpu/smt/active ]; then
    smt_active=$(cat /sys/devices/system/cpu/smt/active)
    if [ "$smt_active" -eq 1 ]; then
        hyperthreading="Active"
    else
        hyperthreading="Inactive"
    fi
fi

echo "Hyper Threading: $hyperthreading"
echo "Online CPUs: ${online_cpus}"
echo "Offline CPUs: ${offline_cpus:-None}"