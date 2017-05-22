#!/bin/bash

. ./source.sh

dir=06-Repetition
sys=stackingfault_2x1

runTS $dir/elec elec
runTS $dir $sys
runTBT $dir $sys


    
