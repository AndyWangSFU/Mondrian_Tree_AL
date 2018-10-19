#PBS -N Mondrian_Forest_het
#PBS -M jrgoetz@umich.edu
#PBS -m abe
#PBS -A tewaria_fluxm
#PBS -q fluxm
#PBS -l qos=flux
#PBS -l nodes=1:ppn=15,walltime=48:00:00,pmem=8gb
#PBS -V

# Set output and error directories
#PBS -j oe
#Command to execute MATLAB program

if [ -s "$PBS_NODEFILE" ]; then
    echo "Running on"
    uniq -c $PBS_NODEFILE
fi

if [ -d "$PBS_O_WORKDIR" ]; then
    cd $PBS_O_WORKDIR
    echo "Running from $PBS_O_WORKDIR"
fi

python run_het_forest_para.py