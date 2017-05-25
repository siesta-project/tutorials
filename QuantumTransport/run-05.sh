#!/bin/bash

. ./source.sh

dir=05-kConv
sys=stackingfault

runTS $dir/elec elec
runTS $dir $sys

pushd $dir
source ./source.sh
for k in 4 8 12 ; do
    tbtkgrid $sys.fdf $k
    runTBT ./ $sys
    mv $sys.TBT.AVTRANS* $sys-k-$k.AVTRANS
    # Clean-up to enable next calculation
    rm *.TBT.nc
    mv $sys.tbt-out $sys-k-$k.tbt-out
done
popd


    
