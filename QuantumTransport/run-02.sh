#!/bin/bash

. ./source.sh

dir=02-SF
sys=stackingfault

runTS $dir/elec elec
runTS $dir $sys
runTBT $dir $sys


    
