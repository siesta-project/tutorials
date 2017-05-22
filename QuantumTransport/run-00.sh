#!/bin/bash

. ./source.sh

dir=00-Chain
sys=chain

runTS $dir/elec elec
runTS $dir $sys
runTBT $dir $sys
runS $dir/siesta $sys

# Calculate the DOS from siesta
pushd $dir/siesta
# -f == shift 0 to fermi-level 
# -m == lowest energy calculated
# -M == highest energy calculated
# -k == tell the program how the k-points are weighted
Eig2DOS -f -m -10. -M 10. -k $sys.KP $sys.EIG > $sys.DOS
popd

# Plot the DOS, transmission and siesta DOS
xmgrace -legend load -nxy $dir/chain.TBT.AVTRANS* $dir/siesta/$sys.DOS &

gnuplot -p -e "plot '$dir/chain.TBT.AVTRANS_Left-Right' u 1:4 w l, '$dir/siesta/chain.DOS' u 1:4 w l" &
