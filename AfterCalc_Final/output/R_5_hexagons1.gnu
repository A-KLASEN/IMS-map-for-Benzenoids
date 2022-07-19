set term pngcairo transparent truecolor size 615.3846153846155, 600 font "Default, 10" 
set output "R_5_hexagons1.png" 
set encoding iso_8859_1 
# 
set multiplot 
# 
set xrange [-6.337441:5.662559] 
set yrange [-6.200108:5.499892] 
set zrange [-20:200] 
set view map 
# 
set cbrange [-5:20] 
set xtics -7,2,6 
set ytics -7,2,6 
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
splot "R_5_hexagons1.dat" index 0 u 1:2:3 w l lt 1 notitle 
# 
reset session 
# 
set xrange [-6.337441:5.662559] 
set yrange [-6.200108:5.499892] 
set zrange [-20:200] 
set ticslevel 0 
set view map 
set linetype 1 lw 1 lc "black60" 
splot "R_5_hexagons1.dat" index 1:40 using 1:2:3 with lines notitle 
# 
unset multiplot 
