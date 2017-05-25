#!/bin/bash

. ./source.sh

clean() {
   pushd $1
   cleanTS $2
   popd
}
clean 00-Chain/elec elec
clean 00-Chain chain
clean 00-Chain/siesta chain
clean 01-Chain/elec elec
clean 01-Chain chain
clean 02-SF/elec elec
clean 02-SF stackingfault
#clean 04-ContourConv/elec elec
#clean 04-ContourConv chain
clean 05-kConv/elec elec
clean 05-kConv stackingfault
clean 06-Repetition/elec elec
clean 06-Repetition stackingfault_2x1
#clean 07-PotDiff/elec elec
#clean 07-PotDiff/0V stackingfault
#clean 07-PotDiff/0.5V stackingfault
#pushd 07-PotDiff
#rm cubediff grid2cube *.cube *.dat
popd

pushd 08-Graphene
clean ac/elec elec
clean ac graphene
clean zz/elec elec
clean zz graphene



