#!/bin/sh
#
# Submit a job in krypton cluster. J.M.Soler, Nov.2012
# Takes job name and number of nodes as input variables

# Set my options for krypton cluster
SIESTA=/home/jose/Siesta/trunk/Obj/siesta
OPTS='--mca btl ^openib,udapl'

# Get input variables
name=$1
nodes=$2

# Check that run directory does not exist
if [ -d $name ] ; then
  echo "Directory $name exists..."
  exit
fi

# Write runfile
echo mpirun $OPTS -n $nodes $SIESTA '<' $name.fdf '>' $name.out > $name.runfile

# Submit job
psub $nodes $name.job $name.runfile $name.dir

