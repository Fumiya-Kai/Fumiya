#　２量子ビット（２つの改良版量子井戸）のラビ振動
import math
import cmath
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate
import numpy as np
import numpy.linalg as LA

#全体設定
plt.rcParams['font.family'] = 'Times New Roman' #フォント
plt.rcParams['font.size'] = 12 #フォントサイズ

#複素数
I = 0.0 + 1.0j


#　物理定数
#プランク定数
h = 6.6260896 * 10**-34
hbar = h / (2.0 * math.pi)
#電子の質量
me = 9.10938215 * 10**-31
#電子ボルト
eV = 1.60217733 * 10**-19
#電気素量
e = 1.60217733 * 10**-19
#光速
c = 2.99792458E+8
#真空の透磁率
mu0 = 4.0 * math.pi * 1.0E-7
#真空の誘電率
epsilon0 = 1.0 / (4.0 * math.pi * c * c) * 1.0E+7


#　物理系の設定
#量子井戸の幅
L = 1.0 * 10**-9
#２つの井戸の中心距離
R = 2.0E-9 #2nm
#計算区間
x_min = -L / 2.0
x_max = L / 2.0
#空間分割数
NX = 500
#空間刻み間隔
dx = 1.0 * 10**-9
#状態数
n_max = 5
#行列の要素数
DIM = n_max + 1
#基底状態・第１励起状態・第２励起状態・第３励起状態
N = 4
#壁の厚さ
W = L / 5
#壁の高さ（単位:eV）
V_H = 30.0
#静電場の強さ
Ex = 10.0E+7
#入射電磁波ベクトルポテンシャルの振幅
A0 = 1.0E-8

#時間間隔
dt = 1.0E-18
#計算ステップ数
Tn = 10000000000
#スキップ数
skip =  10000000

#静電場によるポテンシャル
def phi1(x1, Ex):
    return e * Ex * x1 / eV 

def phi2(x2, Ex):
    return e * Ex * x2 / eV

#クーロン相互作用ポテンシャル項[eV]
def V12(x1, x2):
	return e * e / (4.0 * math.pi * epsilon0)/( abs(x2 - x1) ) / eV

#独立量子井戸の固有関数
def varphi1(n1, x, R, L):
	kn = math.pi * (n1 + 1) / L
	return math.sqrt(2.0 / L) * math.sin( kn * (x + L / 2.0 + R / 2.0 ))

#独立量子井戸の固有関数
def varphi2(n2, x, R, L):
	kn = math.pi * (n2 + 1) / L
	return math.sqrt(2.0 / L) * math.sin(kn * (x + L / 2.0 - R / 2.0))

#独立量子井戸の固有関数の積
def varphi12(n1, n2, x1, x2, R, L):
	return varphi1(n1, x1, R, L) * varphi2(n2, x2, R, L)

#独立量子井戸の固有エネルギー[eV]
def Energy0_12(n1, n2, L):
	kn1 = math.pi * (n1 + 1) / L
	kn2 = math.pi * (n2 + 1) / L
	En1 = hbar**2 * kn1**2 / (2.0 * me)
	En2 = hbar**2 * kn2**2 / (2.0 * me)
	return (En1 + En2) /eV

#2量子ビットの固有状態
def Qbit_varphi(x1, x2, an, n_max, R, L):
	phi=0
	for m1 in range(0,DIM):
		for m2 in range(0,DIM):
			m = m1 * ( n_max + 1 ) + m2
			phi += an[m] * varphi12(m1, m2, x1, x2, R, L)
	return phi

#確率密度分布
def rho(x, an, n_max, R, L):
	if(x <= - R / 2.0 + L / 2.0):
		x_min = R / 2 - L / 2
		x_max = R / 2 + L / 2
		#ガウス・ルジャンドル積分
		result = integrate.quad(
			integral_varphi_x2,    #被積分関数
			x_min,x_max,           #積分区間の下端と上端
			args=(n_max,x,R,L,an)  #被積分関数へ渡す引数
		)
	elif( R / 2.0 - L / 2.0 <= x):
		x_min = - R / 2 - L / 2
		x_max = - R / 2 + L / 2
		#ガウス・ルジャンドル積分
		result = integrate.quad(
			integral_varphi_x1,    #被積分関数
			x_min,x_max,           #積分区間の下端と上端
			args=(n_max,x,R,L,an)  #被積分関数へ渡す引数
		)
	real = result[0]
	return real

#被積分関数[eV]
def integral_V12(x2, x1, n1, n2, m1, m2, R, L, W, V_H, Ex):
	return varphi12(n1, n2, x1, x2, R, L) * bar_V12(x1, x2, R, L, W, V_H, Ex) * varphi12(m1, m2, x1, x2, R, L)

#密度分布計算用の被積分関数
def integral_varphi_x1(x1, n_max, x, R, L, an):
	varphi = Qbit_varphi(x1, x, an,n_max, R, L)
	return abs(varphi)**2

#密度分布計算用の被積分関数
def integral_varphi_x2(x2, n_max, x, R, L, an):
	varphi = Qbit_varphi(x, x2, an, n_max, R, L)
	return abs(varphi)**2

def integral_Xmn(x1, x2, n1, n2, R, L, n_max, an):
    #X = Qbit_varphi(x1, x2, an[n1], n_max, R, L) * (x1 + x2) * Qbit_varphi(x1, x2, an[n2], n_max, R, L)
    return Qbit_varphi(x1, x2, an[n1], n_max, R, L) * Qbit_varphi(x1, x2, an[n2], n_max, R, L)

#ポテンシャル障壁[eV]
def bar_V1(x, R, L, W, V_H ):
	if( x <= - R / 2.0 - W / 2.0 ):
		return 0
	elif( x<= - R / 2.0 + W / 2.0 ):
		return V_H
	else:
		return 0

#ポテンシャル障壁[eV]
def bar_V2(x, R, L, W, V_H ):
	if( x <= R / 2.0 - W / 2.0 ):
		return 0
	elif( x <= R / 2.0 + W / 2.0 ):
		return V_H
	else:
		return 0

#改良版相互作用ポテンシャル
def bar_V12(x1, x2, R, L, W, V_H, Ex ):
	return V12(x1, x2) + bar_V1(x1, R, L, W, V_H) + bar_V2(x2, R, L, W, V_H) + phi1(x1, Ex) + phi2(x1, Ex)

#存在確率分布グラフ描画用の配列初期化
xs = []
phi = [0] * N
for n in range( len(phi) ):
	phi[n] = [0] * (NX + 1)


#　ルンゲクッタクラス
class RK4:
	
	def __init__(self, N, dt):
		self.dt = dt
		self.N = N
		self.A0 = 0
		self.omega = 0
		self.Energy = [0] * N
		self.bn  = np.array([0+0j] * N) 
		self.dbn = np.array([0+0j] * N)
		
		Xnm = [0+0j] * N 
		for i in range( N ):
			Xnm[ i ] = [0+0j] * N
		self.Xnm = np.array( Xnm )

		self.__a1 = np.array([0+0j] * N)
		self.__a2 = np.array([0+0j] * N)
		self.__a3 = np.array([0+0j] * N)
		self.__a4 = np.array([0+0j] * N)

	#１階微分
	def Db(self, t, bn, out_bn ):
		for n in range( N ):
			
			out_bn[n] = self.Energy[n] / (I * hbar) * bn[n] 
			
			for m in range( N ):
				out_bn[n] += self.A0 * e / hbar / hbar * math.cos(self.omega * t) * (self.Energy[n] - self.Energy[m]) * self.Xnm[n][m] * bn[m]

	#時間発展
	def timeEvolution(self, t):
		
		self.Db( t, self.bn, self.__a1 )
		self.Db( t, self.bn + self.__a1 * 0.5 * self.dt, self.__a2 )
		self.Db( t, self.bn + self.__a2 * 0.5 * self.dt, self.__a3 )
		self.Db( t, self.bn + self.__a3 * self.dt, self.__a4 )
		self.dbn = (self.__a1 + 2.0 * self.__a2 + 2.0 * self.__a3 + self.__a4) * self.dt / 6.0



#　計算開始
DIM1 = n_max + 1
DIM2 = DIM1 * DIM1

#積分区間の設定
x1_min = -R / 2.0 - L / 2.0
x1_max = -R / 2.0 + L / 2.0
x2_min = R / 2.0 - L / 2.0
x2_max = R / 2.0 + L / 2.0

#エルミート行列の設定
matrix = [[0]*DIM2 for i in range(DIM2)]

for m1 in range(DIM1):
	for m2 in range(DIM1):
		for n1 in range(DIM1):
			for n2 in range(DIM1):
				#ガウス・ルジャンドル２重積分
				result = integrate.dblquad(
					integral_V12,   #被積分関数
					x1_min, x1_max,                       #第１引数に対する積分区間の下端と上端
					lambda x : x2_min, lambda x : x2_max, #第２引数に対する積分区間の下端と上端
					args=(n1, n2, m1, m2, R, L, W, V_H, Ex)   #被積分関数へ渡す引数
				)
				V_real = result[0]
				V_imag = 0j
				#ターミナルへ出力
				print(f'{m1},{m2},{n1},{n2}, {V_real}')
				#行列要素
				nn = n1 * DIM1 + n2
				mm = m1 * DIM1 + m2
				matrix[mm][nn] = V_real + V_imag
				#対角成分
				if(nn == mm): matrix[mm][nn] += Energy0_12(n1, n2, L)


matrix = np.array( matrix )
#固有値と固有ベクトルの計算
result = LA.eig( matrix )
eig = result[0] #固有値
vec = result[1] #固有ベクトル

index = np.argsort( eig )
eigenvalues = eig[ index ]

vec = vec.T

vectors = vec[ index ]


sum = 0
for i in range(DIM):
	v = matrix @ vectors[i] - eigenvalues[i] * vectors[i]
	for j in range(DIM):
		sum += abs(v[j])**2
print("|MA-EA| =" + str(sum))

#基底状態・第１励起状態・第２励起状態・第３励起状態の存在確率の空間分布
for n in range( N ):
	x_min = -R / 2 - L / 2
	x_max = R / 2 + L / 2
	for nx in range(NX+1):
		x = x_min + (x_max - x_min) / NX * nx
		if( n == 0 ): xs.append(x/dx)
		if( x <= - R / 2.0 + L / 2.0 ):
			phi[n][nx] = rho(x, vectors[n], n_max, R, L) * 1E-9
		elif( R / 2.0 - L / 2.0 <= x ):
			phi[n][nx] = rho(x, vectors[n], n_max, R, L) * 1E-9
		else: 
			phi[n][nx] = 0

#エネルギー差
dE = (eigenvalues[1] - eigenvalues[0]) * eV
#エネルギー差に対応する光子の角振動数
omega = dE / hbar
#電磁波の波長
_lambda =  2.0 * math.pi * c / omega
print( "エネルギー（基底状態）" + str( eigenvalues[0] / eV ) + "[eV]" )
print( "エネルギー（励起状態）" + str( eigenvalues[1] / eV ) + "[eV]" )
print( "エネルギー差" + str( dE /eV ) + "[eV]" )
print( "エネルギー差に対応する光子の角振動数" + str( omega ) + "[rad/s]" )
print( "エネルギー差に対応する光子の角振動数に対する周期" + str( 2.0 * math.pi / omega  ) + "[s]" )
print( "電磁波の波長" + str( _lambda / 1.0E-9  ) + "[nm]" )



rk4 = RK4(N, dt)
#電磁波の角振動数
rk4.omega = omega
#入射電磁波ベクトルポテンシャルの振幅
rk4.A0 = A0
#エネルギー固有値
rk4.Energy[0] = eigenvalues[0] * eV
rk4.Energy[1] = eigenvalues[1] * eV
rk4.Energy[2] = eigenvalues[2] * eV
rk4.Energy[3] = eigenvalues[3] * eV

#Xnmの計算
for n1 in range(N):
	for n2 in range(N):
		x1_min = -R / 2.0 - L / 2.0
		x1_max = -R / 2.0 + L / 2.0
		x2_min = R /2.0 - L / 2.0
		x2_max = R /2.0 + L / 2.0
		#ガウス・ルジャンドル２重積分
		result = integrate.dblquad(
			integral_Xmn,   #被積分関数
			x1_min, x1_max,                       #第１引数に対する積分区間の下端と上端
			lambda x : x2_min, lambda x : x2_max, #第２引数に対する積分区間の下端と上端
			args = (n1, n2, R, L, n_max, vectors)   #被積分関数へ渡す引数
		)
		real = result[0]
		imag= 0
		rk4.Xnm[n1][n2] = real + 1j * imag

		if( abs(real / L) < L ): real = 0
		#ターミナルへ出力
		print( "(" + str(n1) + ", " + str(n2) + ")  " + str( real / L ))

#初期状態の設定
rk4.bn = np.array(
	[ 1.0+0.0j,   #基底状態
	  0.0+0.0j,   #第１励起状態 
	  0.0+0.0j,   #第２励起状態 
	  0.0+0.0j ]  #第３励起状態
)


ts = []
b0s = []
b1s = []

#展開係数の時間依存性の計算
for tn in range(Tn+1):

	t_real = dt * tn
	#計算結果の取得
	if( tn % skip == 0 ): 
		print("t =" + str(tn / skip) + "  " + str(abs(rk4.bn[0])**2))
		
		ts.append( tn / skip )
		#基底状態の存在確率
		b0s.append( abs(rk4.bn[0])**2 )
		#第１励起状態の存在確率
		b1s.append( abs(rk4.bn[1])**2 )

	#ルンゲ・クッタ法による時間発展
	rk4.timeEvolution( t_real )
	#展開係数を更新
	rk4.bn += rk4.dbn

# グラフ描画
plt.title("Expansion coefficient at time")
plt.xlabel("time[s]")
plt.ylabel("Expansion coefficient")

plt.xlim([0,Tn/skip])
plt.ylim([0,1])

plt.plot(ts, b0s, marker="o" , linewidth=3.0)
plt.plot(ts, b1s, marker="o",  linewidth=3.0)


for n in range(N):
	#グラフの描画（基底状態～第３励起状態）
	fig2 = plt.figure(figsize=(10, 6))
	plt.title("Existence probability at Position (n=" + str(n) + ")")
	plt.xlabel("Position[nm]")
	plt.ylabel("|phi|^2")
	
	plt.xlim([-1.5, 1.5])
	plt.ylim([0, 5])
	nEx = 0 
	plt.plot(xs, phi[n], linewidth = 3)

plt.show()
