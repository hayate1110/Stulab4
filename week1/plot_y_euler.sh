gnuplot << EOF
set terminal pngcairo size 1280,720
set output "y_euler.png"
set format x ""
set format y ""
set label 1 "(x_{i+1}, y_{i+1})" at 7.1, 50
set label 2 "(x_{i+1}, y_{i+1}')" at 7.1, 45
set label 3 "(x_i, y_i)" at 5.1, 25
set label 4 "x_i" at 5, -1.5
set label 5 "x_{i+1}" at 7, -1.5
set label 6 "{/Symbol t}" at 6, 9
set style arrow 1 filled heads
set arrow 1 from 5,10 to 7,10 arrowstyle 1

y(x) = x**2

plot[0:10] y(x) linecolor "black", "data2.dat" using 3:4 with impulse title "" linecolor "black", "data2.dat" using 1:2 with lines title "" linecolor "black", "data2.dat" title "" lc "grey10" lt 5, "< echo 7 49" title "" lc "grey10" lt 5
EOF