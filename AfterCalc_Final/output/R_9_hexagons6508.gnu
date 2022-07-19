set term pngcairo transparent truecolor size 600, 838.8349514563106 font "Default, 10" 
set output "R_9_hexagons6508.png" 
set encoding iso_8859_1 
# 
set multiplot 
# 
set xrange [-5.154317:5.145683] 
set yrange [-7.248955:7.151045] 
set zrange [-20:200] 
set view map 
# 
set cbrange [-5:20] 
set xtics -6,2,6 
set ytics -8,2,8 
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
splot "R_9_hexagons6508.dat" index 0 u 1:2:3 w l lt 1 notitle 
# 
reset session 
# 
set xrange [-5.154317:5.145683] 
set yrange [-7.248955:7.151045] 
set zrange [-20:200] 
set ticslevel 0 
set view map 
set linetype 1 lw 1 lc "black60" 
splot "R_9_hexagons6508.dat" index 1:52 using 1:2:3 with lines notitle 
# 
unset multiplot 
