#!/bin/sh
#
#  run_script for basis optimization
#
#  Takes a name as parameter.
#
SIESTA=siesta
#
#
name=$1
#
if [ -d $name ] ; then
  echo "Directory $name exists..."
  exit
fi

mkdir $name
sed -f $name.sed TEMPLATE > $name/$name.fdf
cp *.psf $name
cd $name
$SIESTA < $name.fdf > $name.out
rm -f *.psf *.xml *.psdump      # Optional. To save space
cp BASIS_ENTHALPY OPTIM_OUTPUT
#---------
cd ..
