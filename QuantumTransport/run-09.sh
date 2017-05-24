#!/bin/bash

. ./source.sh

dir=09-IV
sys=stackingfault

pushd $dir

# First calculate the electrode
pushd elec
echo "Calculating the electrode..."
$_ts < elec.fdf > elec.out
[ $? -ne 0 ] && exeDIE $_ts
echo "Done..."
popd

# This will run all biases
setV() {
    local V=$1 ; shift
    sed -i -e "s/TS.Voltage.*/TS.Voltage $V eV/gi" $sys.fdf
    # In principle you need to correct the number of points for
    # tbtrans (due to the bias-window integration).
    # In this case we use a fixed integration seperation
    # which means that you have the same precision for the integral
}

# First we run for the zero bias case (equilibrium)
rm -f $sys.[^f]*
echo "Calculating for 0V..."
setV 0. # set the bias
$_ts < $sys.fdf > $sys.out-V0
[ $? -ne 0 ] && exeDIE $_ts
# Save the density matrix for zero bias (then we can use
# this as a guess for the following bias)
cp $sys.TSDE V0.TSDE
echo "Calculating the current using tbtrans for 0V..."
$_tbt < $sys.fdf > $sys.tbt-out-V0
    [ $? -ne 0 ] && exeDIE $_ts
mv $sys.TBT.AVTRANS* $sys.AVTRANS-V0
rm -f $sys.TBT.nc

# Clean up
rm *.T*GF*

for pm in + - ; do

sign=""
[ "$pm" == "-" ] && sign=$pm

# Restore the density matrix from 0V
cp V0.TSDE $sys.TSDE

for V in 0.15 0.3 0.45 0.6 0.75 0.9 ; do
    echo "Calculating for $sign$V V..."

    setV $sign$V # set the bias
    $_ts < $sys.fdf > $sys.out-V$sign${V//./_}
    [ $? -ne 0 ] && exeDIE $_ts

    echo "Calculating the current using tbtrans for $V V..."
    $_tbt < $sys.fdf > $sys.tbt-out-V$sign${V//./_}
    [ $? -ne 0 ] && exeDIE $_ts
    mv $sys.TBT.AVTRANS_Left-Right $sys.TBT.AVTRANS-V$sign${V//._}
    rm -f $sys.TBT.nc

    # Clean up
    rm *.T*GF*
done

done

# Clean up weird files... ;)
rm INPUT_TMP* fdf-*

# Create the I-V curve
echo "# Bias[V] Current[A]" > IV.dat
for V in -0.9 -0.75 -0.6 -0.45 -0.3 -0.15 0 0.15 0.3 0.45 0.6 0.75 0.9 ; do
    I=`grep '\[A\]' $sys.tbt-out-V${V//./_} | awk '{print $12}'`
    printf "%f\t%f\n" $V $I >> IV.dat
done

echo "Done with collecting information, plot the file IV.dat to see the I-V curve..."

popd
