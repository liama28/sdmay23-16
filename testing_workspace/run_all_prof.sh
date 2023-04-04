echo "Instruction, Time (ms), Instructions (M), Power"
for name in add_mem add fmul imul mov_mem mov mulx_mem mulx sleep prefetchw rdtsc fdiv fsqrt
do
    python3 run.py -p -n profile_${name} profiling_efforts/c_codes/${name}.c >> profile_${name}.txt
    avg_time=$(awk 'NR==20 {print $3}' "profile_${name}.txt")
    num_instr=$(awk 'NR==21 {print $4}' "profile_${name}.txt")
    avg_power=$(awk 'NR==22 {print $4}' "profile_${name}.txt")
    avg_power_values=$(awk 'NR==23 {print $6}' "profile_${name}.txt")
    echo "${name}, ${avg_time}, ${num_instr}, ${avg_power}, ${avg_power_values}"
    sleep 1
done