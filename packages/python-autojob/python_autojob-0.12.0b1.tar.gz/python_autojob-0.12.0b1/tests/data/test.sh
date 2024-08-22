#!/bin/bash
#SBATCH --mail-user=ugn@sfu.ca
#SBATCH --time={{ slurm_time }}
#SBATCH --mail-user=ugn@sfu.ca
#SBATCH --mail-user=ugn@sfu.ca

script_name="${BASH_SOURCE[0]}"
timeline=$(grep -E -m 1 '^#SBATCH[[:space:]]*--time=' "$script_name")
timeslurm=${timeline##*=}
IFS=- read -ra day_split_time <<< "$timeslurm"
no_days_time=${day_split_time[1]}
days=${no_days_time:+${day_split_time[0]}}
no_days_time=${day_split_time[1]:-${day_split_time[0]}}
IFS=: read -ra split_time <<< "$no_days_time"

if [[ $days ]]; then
  # D-H, D-H:M, D-H:M:S
  slurm_days="$days"
  slurm_hours=${split_time[0]}
  slurm_minutes=${split_time[1]:-0}
  slurm_seconds=${split_time[2]:-0}
else
  # M, M:S, H:M:S
  slurm_days=0
  if [[ ${#split_time[*]} == 3 ]]; then
    slurm_hours=${split_time[0]}
    slurm_minutes=${split_time[1]}
    slurm_seconds=${split_time[2]}
  else
    slurm_hours=0
    slurm_minutes=${split_time[0]}
    slurm_seconds=${split_time[1]:-0}
  fi
fi

echo "Running for $(echo "$slurm_days*1" |bc)d $(echo "$slurm_hours*1" |bc)h $(echo "$slurm_minutes*1" |bc)m and $(echo "$slurm_seconds*1" |bc)s."
timeslurm=$(echo "$slurm_days*86400 + $slurm_hours*3600 + $slurm_minutes*60 + $slurm_seconds" | bc)
echo "This means $timeslurm seconds."
timeslurm=$(echo "$timeslurm *0.9" |bc)
echo "Will terminate at ${timeslurm}s to copy back necessary files from scratch"

echo ""
echo ""
