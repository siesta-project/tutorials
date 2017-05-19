#set terminal postscript
#set output 'denchar.scf.ps'
set terminal x11 
set output 
set noclip points
set clip one
set noclip two
set border
set boxwidth
set dgrid3d 50,50, 4
set dummy u,v
set format x "%g"
set format y "%g"
set format z "%g"
set nogrid
set nokey  
#set key  
set nolabel
#set label
set noarrow
set nologscale
set offsets 0, 0, 0, 0
set nopolar
set angles radians
set parametric
set view 0, 0, 1, 1
set samples 100, 100
set isosamples 10, 10
set nosurface
set contour base
#set noclabel
set clabel
set nohidden3d
set cntrparam order 4
set cntrparam bspline
set cntrparam levels auto 13
#set cntrparam levels incremental -0.04,0.005,0.04
set cntrparam points 5
set size 0.5089,1
set data style points
set function style lines
set xzeroaxis
set yzeroaxis
set tics in
set ticslevel 0.5
set noxtics
set noytics
set noztics
#set xtics
#set ytics
#set ztics
#set title "" 0,0
#set title "Charge density. FeSi (CsCl struct.). a = 2.77 A" 
#set label "Si" at 0,0
set notime
set rrange [-0 : 10]
set trange [-5 : 5]
set urange [-5 : 5]
set vrange [-5 : 5]
set xlabel "" 0,0
set xrange [0.78375 : 6.78375]
set ylabel "" 0,0
set yrange [2.21679 : 8.21679]
set zlabel "" 10,0
set zrange [9.83867e-05 : 0.00419016]
set autoscale r
set autoscale t
set autoscale xy
set autoscale z
set zero 1e-08
#splot 'Si.CON.SCF' using 1:2:3 with lines
splot "sin(x*y)" using 1:2:3 with lines
