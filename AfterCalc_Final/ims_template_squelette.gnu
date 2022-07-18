set term pngcairo transparent truecolor size 794.1176470588236, 600 font "Default, 10" 
set output "TEST.png"
set encoding iso_8859_1 
#
set multiplot
#
set xrange [-7.265483:6.234517] 
set yrange [-5.585876:4.614124] 
set zrange [-20:200] 
set view map 
#
set cbrange [-5:20] 
set xtics -8,2,7 
set ytics -6,2,5 
set ztics -5,5,25 
set mytics 1 
set mxtics 1 
set isosample 500, 500 
set cont base 
set cntrparam level incremental 0,5,20 
unset surf 
unset key
set palette model RGB defined (-5 '#FFE5CC', 0 '#FFFFFF', 20 '#C0C0DF') 
set palette maxcolors 5 
set xlabel "x ({\305})" font "Times-Roman, 10" #offset 0,-1 
set ylabel "y ({\305})" font "Times-Roman, 10" #offset 0,-1 
set pm3d 
unset clabel 
set linetype 1 lw 1.5 lc "grey60" 
splot "R_5_hexagons3.dat" index 0 u 1:2:3 w l lt 1 notitle
#
reset session
#
set xrange [-7.265483:6.234517] 
set yrange [-5.585876:4.614124] 
set zrange [-20:200] 
set ticslevel 0
set view map
set linetype 1 lw 1 lc "black60" 
splot "R_5_hexagons3.dat" index 1:40 using 1:2:3 with lines notitle
#
unset multiplot