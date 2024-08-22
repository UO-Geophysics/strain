from numpy import genfromtxt,zeros,where
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator
from mudpy import gmttools,view
import numpy as np

plt.rcParams["font.family"] = "Helvetica"

faults_to_plot=1# 1 to 5main,synth,pian,anti,detach
#Run time parameters
home='/Users/dmelgarm/Slip_inv/'

project_name='Turkey2023_M7.5_Surgu2'


# run_name='gnss'
# run_number='0010'
# run_name='gnss_smv_vr5.2'
run_name = 'gnss_smv_vwest_4.8_veast_2.8'
# run_name = 'gnss_smv_vr_2.8'
run_number='0010'

epicenter=np.array([  37.26772 , 38.044004, 16.2943])

meshfile1='/Users/dmelgarm/Slip_inv/Turkey2023_M7.5_Surgu2/data/model_info/3d_fault_M7.5_with_Surgu2.mshout'
meshfile2 = '/Users/dmelgarm/Turkey2023/3d_fault/3d_fault_M7.8.mshout'

maxslip=None
UTM_zone='37S'
fudge=0.01
fake_hypo=[0.1,0.1],
borderwidth=0.5
#figsize=(8,6)
figsize=(12,9)
xtick=0.5
ytick=0.5
ztick=20
inverse_model=False
hypocenter=None
strike=220
azimuth=-103
elevation=36





fault_name=home+project_name+'/output/inverse_models/models/%s.%s.inv' % (run_name,run_number)
gmttools.make_total_model(fault_name,thresh=0)
fault=genfromtxt(home+project_name+'/output/inverse_models/models/%s.%s.inv.total' % (run_name,run_number))
#Parse log file for hypocenter
log_file=home+project_name+'/output/inverse_models/models/%s.%s.log' % (run_name,run_number)
f=open(log_file,'r')
loop_go=True
while loop_go:
    line=f.readline()  
    if 'Mw' in line:
        Mw=float(line.split(':')[-1].split(' ')[-1])   
        loop_go=False
f.close() 
    

def get_corners(meshfile):
    #get subfault corners
    corners=genfromtxt(meshfile,usecols=range(4,13))
    i=where(corners[:,0]>360)[0]
    corners[i,0]=corners[i,0]-360
    i=where(corners[:,3]>360)[0]
    corners[i,3]=corners[i,3]-360
    i=where(corners[:,6]>360)[0]
    corners[i,6]=corners[i,6]-360
    corners[:,2]=-corners[:,2]
    corners[:,5]=-corners[:,5]
    corners[:,8]=-corners[:,8]
    return corners
                
corners1=get_corners(meshfile1)  
corners2=get_corners(meshfile2)  
 
if faults_to_plot==1:
    corners=corners1

Nfaults=len(corners)
    
    
#Normalized slip
slip=(fault[:,8]**2+fault[:,9]**2)**0.5
total_slip=slip

#Saturate to maxslip
if maxslip!=None:
    imax=where(slip>maxslip)[0]
    slip[imax]=maxslip
#normalize
norm_slip=slip/slip.max()

#Get colormaps
# slip_colormap = plt.cm.gist_heat_r
slip_colormap=gmttools.gmtColormap(u'/Users/dmelgarm/code/python/cpt/magma_white.cpt').reversed()
   
fig=plt.figure(figsize=figsize)
ax = fig.add_subplot(111, projection='3d')

#Fenagle the axis ticks
xmajorLocator = MultipleLocator(xtick)
ymajorLocator = MultipleLocator(ytick)
zmajorLocator = MultipleLocator(ztick)
ax.xaxis.set_major_locator(xmajorLocator)
ax.yaxis.set_major_locator(ymajorLocator)
ax.zaxis.set_major_locator(zmajorLocator)
xl=[corners2[:,0].min()-0.2,corners2[:,0].max()]
yl=[corners2[:,1].min(),corners2[:,1].max()+0.2]
zl=[0,25]

ax.set_xlim(xl)
ax.set_ylim(yl)
ax.set_zlim(zl)
ax.set_box_aspect((1,1,0.075))  # aspect ratio is 1:1:1 in data space
ax.invert_zaxis()
ax.view_init(elev=elevation, azim=azimuth)




#Make one patch per subfaultr
for ksub in range(len(corners)):

    vertices=[[tuple(corners[ksub,0:3]),tuple(corners[ksub,3:6]),tuple(corners[ksub,6:9])]]
    subfault=Poly3DCollection(vertices, linewidths=borderwidth)
    subfault.set_color(slip_colormap(norm_slip[ksub]))
    subfault.set_linewidth(borderwidth)
    subfault.set_edgecolor('#505050')
    ax.add_collection3d(subfault)


for ksub in range(len(corners2)):
    #blank M7.5
    vertices=[[tuple(corners2[ksub,0:3]),tuple(corners2[ksub,3:6]),tuple(corners2[ksub,6:9])]]
    subfault=Poly3DCollection(vertices, linewidths=borderwidth)
    subfault.set_color('#D7E5EF')
    subfault.set_linewidth(borderwidth)
    subfault.set_edgecolor('#505050')
    ax.add_collection3d(subfault)

#Dummy mapable for colorbar
s=plt.scatter(zeros(len(total_slip)),zeros(len(total_slip)),c=total_slip,cmap=slip_colormap,s=0.00001,lw=0)

#Mke colorbar
ax_cb2 = fig.add_axes([0.88,0.18,0.01,0.3])
cb=plt.colorbar(s,cax=ax_cb2)
tick_locator = ticker.MaxNLocator(nbins=5)
cb.locator=tick_locator
cb.update_ticks()
cb.set_label('Slip (m)')

#Labels n' stuff
ax.set_xlabel('\n\nLongitude')
ax.set_ylabel('\n\nLatitude')
ax.set_zlabel('z (km)',rotation=90)

#get stf
tstf,stf = view.source_time_function(home+project_name+'/output/inverse_models/models/%s.%s.inv' % (run_name,run_number),epicenter,plot=False)


ax2 = fig.add_axes([0.51,0.32,0.22,0.19])
ax2.fill_between(tstf,np.zeros(len(stf)),stf,color='#20B2AA')
ax2.plot(tstf,stf,'k',lw=2)
ax2.set_xlabel('Seconds after OT')
ax2.set_ylabel(r'$10^{19}$ Nm/s')
ax2.grid()
ax2.set_xticks([0,15,30])
ax2.set_xlim([-2,30])


#Reference towns
x = 36.186 ; y = 36.584 
dl=0.05
s = 'Ískenderun'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x+1*dl, y+dl, 0, s, zdir=[1,1.35,0],fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))


#Reference towns
x = 35.969 ; y = 37.181 
dl=0.05
s = 'Adana'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x+1.5*dl, y+dl, 0, s, zdir='y',fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))

#Reference towns
x = 37.378 ; y = 37.062 
dl=0.05
s = 'Gaziantep'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x+0.3*dl, y+2.2*dl, 0, s, zdir=[1,0.6,0],fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))

#Reference towns
x = 36.263 ; y = 37.095 
dl=0.05
s = 'Osmaniye'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x-0.5*dl, y+2*dl, 0, s, zdir='y',fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))

x = 36.461 ; y = 37.243 
dl=0.05
s = 'Düziçi'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x+1.5*dl, y+dl, 0, s, zdir='y',fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))


x = 36.9184 ; y = 37.5829 
dl=0.05
s = 'Kahramanmaraş'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x-0*dl, y+10*dl, 0, s, zdir='x',fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))
ax.plot([x,x],[y,y+11*dl],[0,0],'k',lw=1,zorder=9999)

x = 38.307 ; y = 38.359 
dl=0.05
s = 'Malatya'
ax.scatter(x,y,0,marker='o',s=50,edgecolor='k',facecolor='g',zorder=9999)
ax.text(x-dl, y-4.5*dl, 0, s, zdir=[1,0.3,0],fontsize=12,zorder=9999,
        bbox=dict(facecolor='white', edgecolor='k', boxstyle='round'))

plt.subplots_adjust(bottom=-0.1,top=1.1,left=-0.1,right=0.99)

plt.show()