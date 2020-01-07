import matplotlib.pyplot as plt
import math
import csv
x = [] #原始 data X
y = [] #原始 data y
pb = [] #選取的 blank 兩個點
pf = [] #選取的 film 兩個點
xb = [] #選取 blank X
yb = [] #選取 blank y
xf = [] #選取 film X
yf = [] #選取 film y
value_i = []
value_j = []
value_k = []
value_l = []
percent_5 = []
percent_20 = []
percent_10 = []

 

#讀取excel檔案-----------------------------------------------------------------
with open('import_profile.csv', newline='') as csvfile:
    n = input('請輸入間距: ')
    n = float(n)
    datas = csv.reader(csvfile)
    for data in datas:
        x.append(float(data[0])/n)
        y.append(float(data[1]))
im1 = plt.plot(x, y) #劃出profile 圖

#使用者選取並定義 blank 及 film範圍---------------------------------------------
pb.append(plt.ginput(2))
pf.append(plt.ginput(2))
xb = x[int(pb[0][0][0]) : int(pb[0][1][0])]
yb = y[int(pb[0][0][0]) : int(pb[0][1][0])]
xf = x[int(pf[0][0][0]) : int(pf[0][1][0])]
yf = y[int(pf[0][0][0]) : int(pf[0][1][0])]
thk_mean = sum(yb)/len(yb) #blank平均厚度
plt.show(im1)

#求眾數-----------------------------------------------------------------------
def get_mode(yf):
    mode = [];
    yf_appear = dict((a, yf.count(a)) for a in yf)
    if max(yf_appear.values()) == 1:
        return
    else:
        for k, v in yf_appear.items():
            if v == max(yf_appear.values()):
                mode.append(k)
    return mode
thk_mode = sum(get_mode(yf))/len(get_mode(yf))

#求中心厚度-------------------------------------------------------------------
def get_median(yf):
    yf = sorted(yf)
    size = len(yf)
    if size % 2 == 0:
        median = (yf[size//2] + yf[size//2-1])/2
        yf[0] = median
    if size % 2 == 1:
        median = yf[(size-1)//2]
        yf[0] = median
    return yf[0]

#開始算U%---------------------------------------------------------------------
def Interval(a, b):
    value = []
    for i in yf:
        if i - thk_mode >= thk_mode*a:
            if i - thk_mode < thk_mode*b:
                value.append(1)
    return value
 
def percentage(a, b):
    ans =  100*len(Interval(a, b))/len(yf)
    return ans

va = percentage(-0.1, -0.075)
vb = percentage(-0.075, -0.05)
vc = percentage(-0.05, -0.025)
vd = percentage(-0.025, 0)
ve = percentage(0, 0.025)
vf = percentage(0.025, 0.05)
vg = percentage(0.05, 0.075)
vh = percentage(0.075, 0.1)

 
for i in yf:
    if i - thk_mode < thk_mode*-0.15:
        value_i.append(1)
    if i - thk_mode > thk_mode*0.15:
       value_j.append(1)
    if i - thk_mode < thk_mode*-0.1:
        value_k.append(1)
    if i - thk_mode > thk_mode*0.1:
        value_j.append(1)
    if abs(i-thk_mode) < 0.005:
        percent_5.append(1)
    if abs(i-thk_mode) > 0.02:
        percent_20.append(1)
    if abs(i-thk_mode) < 0.01:
        percent_10.append(1)

vi = 100*(len(value_i)/len(yf))
vj = 100*(len(value_j)/len(yf))
vk = 100*(len(value_k)/len(yf))
vl = 100*(len(value_l)/len(yf))

vpercent_5 = 100*(len(percent_5)/len(yf))
vpercent_20 = 100*(len(percent_20)/len(yf))
vpercent_10 = 100*(len(percent_10)/len(yf))
#----------------------------------------------------------------------------

u = [va+vb+vc+vd, vb+vc+vd+ve, vc+vd+ve+vf, vd+ve+vf+vg, ve+vf+vg+vh]
#print('blank平均厚度為:', thk_mean)
#print('短軸膜面厚度的眾數為:', thk_mode)
print('中心厚度為: ', int(10000*(get_median(yf))), 'A')
#print('各區間總合為:', math.ceil(va+vb+vc+vd+ve+vf+vg+vh+vk+vl+vi+vj), '%')
#print('-10%~0%為: ', u[0])
#print('-7.5%~-2.5%為: ', u[1])
#print('-5%~5%為: ', u[2])
#print('-2.5%~7.5%為: ', u[3])
#print('0%~10%為: ', u[4])
print('<10%為: ', max(u))
print('>30%為: ', vi+vj)
print('<5nm為: ', vpercent_5)
print('>20nm為: ', vpercent_20)
print('<10nm為: ', vpercent_10)
 
new = list(zip(xb, yf))
x0 = []
y0 = []
for i in new:
    x0.append(i[0])
    y0.append(i[1])
plt.plot(xb, yb)
plt.plot(x0, y0)
plt.show()