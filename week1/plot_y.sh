gnuplot << EOF
set terminal png
set output "y.png"
set format x ""
set format y ""
set label 1 "x_0" at 5, -1
set label 2 "x_1" at 6, -1
set label 3 "x_2" at 7, -1
set label 4 "x_3" at 8, -1
set label 5 "y_0" at 0, 27
y(x) = x**2
plot[0:10] y(x) linecolor "black", "data1.dat" using 1:2 with impulse title "" linecolor "black", "data1.dat" using 3:4 with lines title "" linecolor "black"
EOF