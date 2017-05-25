#!/bin/bash

. ./source.sh

dir=01-Chain
sys=chain

runTS $dir/elec elec
runTS $dir $sys
runTBT $dir $sys
