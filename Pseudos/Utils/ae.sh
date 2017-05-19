#!/bin/sh -f
#
# ae.sh -- Script to run all-electron atomic calculations
#
# Usage: ae.sh <name.inp>
#
DEFAULT_DIR=../../Utils
ATOM_UTILS_DIR=${ATOM_UTILS_DIR:-${DEFAULT_DIR}}
#
default="../../../atm"
prog=${ATOM_PROGRAM:-$default}
#
if [ "$#" != 1 ] 
then
	echo "Usage: $0 <name.inp>"
	exit
fi
#
file=$1
name=`basename $1 .inp`
#
#
if [ -d $name ] 
then
	echo "Directory $name exists. Please delete it first"
	exit
fi
#
mkdir $name ; cd $name
cp ../$file ./INP
#
# This speeds up calculations with the van der Waals functional
# The environmental variable has to be set in advance, or in
# the command-line itself, as in
#
# VDW_KERNEL_TABLE=/some/path/to/vdw_kernel.table sh ae.sh File.inp
#
if [ -r "$VDW_KERNEL_TABLE" ]
then
        cp $VDW_KERNEL_TABLE ./vdw_kernel.table
        echo "Copying vdw kernel table from $VDW_KERNEL_TABLE"
fi
#
$prog
#
echo "==> Output data in directory $name"
#
#
#  Copy relevant plotting scripts
#
for i in charge vcharge vspin ae ; do
        cp -f ${ATOM_UTILS_DIR}/$i.gps .
	cp -f ${ATOM_UTILS_DIR}/$i.gplot .
done
#


