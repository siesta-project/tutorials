#!/bin/bash

if [ "$#" -ne 5 ]
then
    echo "Usage $0 File.in lat_min lat_max incremet cell_type(sc,bcc,fcc,diamond)"
    exit
fi

file=$1;
latMin=$2;
latMax=$3;
disp=$4;
cell=$5;


#############################################
steps=$(echo "($latMax-$latMin)/$disp" |bc);
let steps=steps+1;

echo $steps;

lat=$latMin;
l=0;
#############################################

rm -f murnaghan.in;
echo $cell > murnaghan.in;

while [ $l -lt $steps ];
  do

  sed -e "s/lat/$lat/" $file.in > $file.fdf ;

    #Filtered
  siesta < $file.fdf >& $file-$lat.out;
  EF=$(awk '/Total =/{print $4}' $file-$lat.out);
  echo $lat $EF  >> "murnaghan.in";

  echo "      " $lat $EF
  
  rm -rf INPUT*;
  
  let l=l+1
  lat=$(echo  "scale=5; $lat+$disp"|bc);

done

/opt/local/bin/python latcon.py murnaghan.in;




