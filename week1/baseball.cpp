// baseball.cpp: オイラー法を用いて野球ボールの軌道を計算するプログラム 
#include "NumMeth.h"

using namespace std;
int main() {
//* ボールの初期位置及び初期速度を設定する.
double y1, speed, theta;
double r1[2+1], v1[2+1], r[2+1], v[2+1], accel[2+1]; cout << "高さの初期値(メートル) : "; cin >> y1;
r1[1] = 0; 
r1[2] = y1; // 初期位置ベクトル
cout << "初期速度(m/s) : "; cin >> speed;
cout << "初期角度(度) : "; cin >> theta;
const double pi = 3.141592654;
v1[1] = speed*cos(theta*pi/180); // 初期速度 (x)
v1[2] = speed*sin(theta*pi/180); // 初期速度 (y)
r[1] = r1[1]; 
r[2] = r1[2]; // 初期位置および初期速度を設定 
v[1] = v1[1]; 
v[2] = v1[2];
//* 物理パラメータを設定(質量, Cd 値など)
double Cd = 0.35;
double area = 4.3e-3;
double grav = 9.81;
double mass = 0.145;
double airFlag, rho;
cout << "空気抵抗(あり:1, なし:0) : "; 
cin >> airFlag; if( airFlag == 0 )
rho = 0; // 空気抵抗なし else
rho = 1.2; // 空気の密度(kg/m^3)
double air_const = -0.5*Cd*rho*area/mass; // 空気抵抗定数
//* ボールが地面に着くまで, あるいは最大の刻み数になるまでループ 
double tau;
cout << "時間刻み τ(秒) : "; cin >> tau;
int iStep, maxStep = 1000; // 最大の刻み数
double *xplot, *yplot, *xNoAir, *yNoAir; 
xplot = new double [maxStep + 1];
yplot = new double [maxStep + 1]; 
xNoAir = new double [maxStep + 1]; 
yNoAir = new double [maxStep + 1];

double max_y = 0;

for( iStep=1; iStep<=maxStep; iStep++ ) {
    //* プロット用に位置(計算値および理論値)を記録する
    xplot[iStep] = r[1]; // プロット用に軌道を記録 
    yplot[iStep] = r[2];
    double t = ( iStep-1 )*tau; // 現在時刻 
    xNoAir[iStep] = r1[1] + v1[1]*t; // 位置(x) 
    yNoAir[iStep] = r1[2] + v1[2]*t - (0.5*grav*t*t); // 位置(y) ここに位置を求める式を書く 
    //* ボールの加速度を計算する
    // 空気抵抗(無次元)
    // 投射物の横断面積(m^2) 
    // 重力加速度(m/s^2)
    // 投射物の質量(kg)
    double normV = sqrt( v[1]*v[1] + v[2]*v[2] );
    accel[1] = air_const*normV*v[1]; // 空気抵抗
    accel[2] = air_const*normV*v[2]; // 空気抵抗
    accel[2] -= grav; // 重力
    //* オイラー法を用いて, 新しい位置および速度を計算する

    r[1] = r[1] + tau*v[1];
    r[2] = r[2] + tau*v[2];
    
    v[1] = v[1] + tau*accel[1];
    v[2] = v[2] + tau*accel[2];

    //* ボールが地面に着いたら(y < 0)ループを抜ける
    /*
    if 文を使って書く
    */ 
    if(yplot[iStep]<0) {
        break;
    }

    if(r[2]>max_y) {
        max_y = r[2];
    }
}
//* 最大到達高さと滞空時間を表示する(このままだと正しい結果ではない) 
cout << "最大到達高さは" << max_y << "メートル" << endl;
// 滞空時間の表示をここに書く
cout << "滞空時間は" << tau*iStep << "秒" << endl;
//* プロットする変数を出力する
// xplot, yplot xNoAir, yNoAir
ofstream xplotOut("xplot.txt"), yplotOut("yplot.txt"),
xNoAirOut("xNoAir.txt"), yNoAirOut("yNoAir.txt");
int i;

for( i=1; i<=iStep; i++ ) {
    xplotOut << xplot[i] << endl;
    yplotOut << yplot[i] << endl; 
}

for( i=1; i<=iStep; i++ ) { 
    xNoAirOut << xNoAir[i] << endl;
    yNoAirOut << yNoAir[i] << endl; 
}

ofstream xyplotOut("xyplot.txt"), xyNoAirOut("xyNoAir.txt");
xyplotOut << "#X Y" << endl;
xyNoAirOut << "#X Y" << endl;

for( i=1; i<=iStep; i++ ) {
    if (i>0 && yplot[i] == 0){
        continue;
    }
    xyplotOut << xplot[i] << " " << yplot[i] << endl;
}

for( i=1; i<=iStep; i++ ) { 
    if (i>0 && yplot[i] == 0){
        continue;
    }
    xyNoAirOut << xNoAir[i] << " " << yNoAir[i] << endl;
}

delete [] xplot;
delete [] yplot;
delete [] xNoAir;
delete [] yNoAir; // メモリを開放
}