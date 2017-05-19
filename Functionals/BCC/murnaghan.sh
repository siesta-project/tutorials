#!/bin/bash

if [ "$#" -ne 6 ]
then
    echo "Usage $0 File.in lat_min lat_max incremet cell_type(sc,bcc,fcc,diamond) label"
    exit
fi


file=$1;
latMin=$2;
latMax=$3;
disp=$4;
cell=$5;
label=$6;


#############################################
steps=$(echo "($latMax-$latMin)/$disp" |bc);
let steps=steps+1;

echo "Number of calls to siesta=" $steps;

lat=$latMin;
l=0;
#############################################

rm -f $label; 
echo $cell > $label;

while [ $l -lt $steps ];
  do

  sed -e "s/lat/$lat/" $file.in > $file.fdf ;


  siesta < $file.fdf >& $file-$lat.out;
  awk '/siesta: FreeEng =/{print $4}' $file-$lat.out > tmp;
  #EF=$(awk  $EF); 
  
  EF=$(awk '//{getline; print $1}' tmp);
  echo $lat $EF  >> $label;

  echo "      " $lat $EF
  
  rm -rf INPUT*;

  vol=$(echo "scale=5; $lat*$lat*$lat/2.0"|bc);

  echo $vol $EF >> E-VS-vol-$label;
  
  let l=l+1
  lat=$(echo  "scale=5; $lat+$disp"|bc);

done

python latcon.py $label;




