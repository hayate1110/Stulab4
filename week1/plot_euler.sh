#!/bin/zsh
g++ -o baseball baseball.cpp
./baseball << EOF
0
40
45
1
$1
EOF

gnuplot << EOF
set terminal pngcairo size 1280,720
set xzeroaxis linetype 0 linewidth 3
set output "tau_$1.png"
plot "xyPlot.txt" w l title "計算値", "xyNoAir.txt" w l title "理論値"
exit
EOF