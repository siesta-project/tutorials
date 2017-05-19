#!/bin/sh -f
#
# pg.sh -- Script to run pseudopotential generation calculations
#
# Usage: pg.sh <name.inp>
#
DEFAULT_DIR=../../../Utils
ATOM_UTILS_DIR=${ATOM_UTILS_DIR:-${DEFAULT_DIR}}
#
default="../../../../atm"
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
# VDW_KERNEL_TABLE=/some/path/to/vdw_kernel.table sh pg.sh File.inp
#
if [ -r "$VDW_KERNEL_TABLE" ]
then
        cp $VDW_KERNEL_TABLE ./vdw_kernel.table
        echo "Copying vdw kernel table from $VDW_KERNEL_TABLE"
fi
#
$prog
#
cp VPSOUT ../$name.vps
cp VPSFMT ../$name.psf
[ -r VPSXML ] && cp VPSXML ../$name.xml
#
echo "==> Output data in directory $name"
echo "==> Pseudopotential in $name.vps and $name.psf (and maybe in $name.xml)"
#
#  Copy plotting scripts
#
for i in charge vcharge vspin coreq pots pseudo subps ; do
            cp -f ${ATOM_UTILS_DIR}/$i.gps .
            cp -f ${ATOM_UTILS_DIR}/$i.gplot .
done



