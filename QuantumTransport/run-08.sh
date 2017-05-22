#!/bin/bash

. ./source.sh

dir=08-Graphene
sys=graphene

source $dir/source.sh

for t in ac zz ; do
    runTS $dir/$t/elec elec
    runTS $dir/$t $sys
    runTBT $dir/$t $sys
    pushd $dir
    for k in 10 20 ; do
	tbtkgrid $sys.fdf $k 1
	runTBT $t $sys
	mv $t/$sys.TBT.AVTRANS* $t/$sys-k-$k.AVTRANS
	mv $t/$sys.tbt-out $t/$sys-k-$k.tbt-out
    done
    tbtkgrid $sys.fdf 10 1
    popd
done

