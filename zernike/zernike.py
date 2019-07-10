from scipy.special import factorial
import scipy
#import numpy as np 

def neumann_factor(m):
    if m==0:
        return(2)
    else:
        return(1)

'''
def OSAindex(n,m):
    j = (n*(n+2)+m)/2
    return(j)
    
def RadialZernike(rho,n,m,outside=0.0):
    R = np.zeros_like(rho)
    m=np.abs(m); #sign of m does not change radial function
    if n<m:
        abort();
    if (n-m) % 2 == 0: # is even?
        kmax = int(0.5*(n-m));
        for k in range(0,kmax+1):
            top = (-1)**k * factorial(n-k);
            bot = factorial(k)
            bot *= factorial(0.5*(n+m)-k)
            bot *= factorial(0.5*(n-m)-k);
            R += (top/bot)*rho**(n-2*k)
        # Treat Function Outside of the Defined Range
        R[rho>1]=outside
        return(R)
    else:
        return(R)
    
def AngularZernike(phi,m):
    phase = np.abs(m) * phi;
    if m<0: # negative
        return(np.sin(phase))
    else:   # non-negative
        return(np.cos(phase))
    
def Zernike(rho,phi,n,m,outside=0):
     return(RadialZernike(rho,n,m,outside=outside)*AngularZernike(phi,m))
    
def CalculateZernikeCoefficient(Phase,n,m,debug=False):
    
    Nx, Ny = np.shape(Phase)
    if debug: print("Dims of phase: ",Nx,Ny)
    if Nx==Ny:
        Resolution=Nx
    else:
        abort()
    if (n-m) % 2 == 0: # is even?
        
        x = np.linspace(-1,1,Resolution);
        y = np.linspace(-1,1,Resolution);
        dx=x[1]-x[0]; 
        dy=y[1]-y[0];
        if debug: print('dx,dy =',dx,dy)
        X,Y = np.meshgrid(x,y)
        R = np.sqrt(X**2+Y**2);
        phi = np.arctan2(Y,X)
        top = 2*n+2
        bot = neumann_factor(m)*np.pi
        if debug: print('top =',top)
        if debug: print('bot =',bot)
        Phase[R>1] = 0.0
        if debug: print('max phase =',np.max(Phase))       
        if debug: print('min phase =',np.min(Phase))  
        if debug:
            import matplotlib.pylab as plt
            plt.figure()
            plt.imshow(Phase,origin='lower')
            plt.colorbar()
            plt.title('Phase')
            
            plt.figure()
            plt.imshow(Zernike(R,phi,n,m,outside=0),origin='lower')
            plt.colorbar()
            plt.title("Z")

            plt.figure()
            plt.imshow(X,origin='lower')
            plt.colorbar()
            plt.title("X")

            plt.figure()
            plt.imshow(Y,origin='lower')
            plt.colorbar()
            plt.title("Y")
            
            plt.figure()
            plt.imshow(R,origin='lower')
            plt.colorbar()
            plt.title("R")
            
            plt.figure()
            plt.imshow(phi,origin='lower')
            plt.colorbar()
            plt.title("phi")
            
            plt.figure()
            plt.imshow(Phase * Zernike(R,phi,n,m,outside=0),origin='lower')
            plt.colorbar()
            plt.title("integrand")
            
        amn=(top/bot)*np.sum(Phase * Zernike(R,phi,n,m,outside=0)*dx*dy)
        return(amn)
    else:
        return(0.0)

    
def ZernikeSpectrum(Phase,nmax=6,Symmetry=None):
    spectrum={}
    spectrum['c']=np.array([])      # coefficient
    spectrum['j']=np.array([])       # OSA Index
    spectrum['n']=np.array([])       # Radial Index
    spectrum['m']=np.array([])       # Angular Index

    for n in range(nmax+1): # go up to nmax
        for m in range(-n,n+1): #range from -n to n
            if (n-m) % 2 == 0: # is even?
                #print(OSAindex(n,m),n,m,amn)
                spectrum['j'] = np.append(spectrum['j'],int(OSAindex(n,m)))
                spectrum['n'] = np.append(spectrum['n'],int(n))
                spectrum['m'] = np.append(spectrum['m'],int(m))
                if Symmetry==None:
                    spectrum['c'] = np.append(spectrum['c'],CalculateZernikeCoefficient(Phase,n,m))
                if Symmetry=='Azimuthal':
                    if m==0:
                        spectrum['c'] = np.append(spectrum['c'],CalculateZernikeCoefficient(Phase,n,m))
                    else:
                        spectrum['c'] = np.append(spectrum['c'],0.0)

                    



    return(spectrum)

def PlotZernikeSpecturm(Spectrum,IncludePiston=False,unit='rad',PlotThreshold=1e-14):
    import matplotlib.pylab as plt
    s = Spectrum;
    if IncludePiston:
        i=0;
    else:
        i=1;
    s['c'][np.abs(s['c'])<=PlotThreshold*np.nanmax(np.abs(s['c']))]=np.nan
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(4,3)
    ax.plot(s['j'][i:],s['c'][i:],'.k')

    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    #ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xticks(np.arange(0,len(s['c']),1),minor=True)
    
    plt.ylim(-1.1*np.nanmax(np.abs(s['c'][i:])),1.1*np.nanmax(np.abs(s['c'][i:])))
    if not unit=='':
        ax.set_ylabel('Zernike Coefficient ('+unit+')')
    else:
        ax.set_ylabel('Zernike Coefficient')
    ax.set_xlabel('j, OSA Index')
    return(fig,ax)




def extract_phase(basename,dims=False):
    
    xps = np.load(basename+'_xps.npy')
    eiks = np.load(basename+'_eiks.npy')
    Nrays = len(eiks[:,0])
    if not dims:
        Nx=int(np.sqrt(Nrays))
        Ny=Nx;
    else:
        Nx=dims[0];
        Ny=dims[1];
    phase = eiks[:,0] + xps[:,4]*xps[:,0]
    phase -= np.min(phase)
    phase = np.reshape(phase,(Nx,Ny))
    return(phase)

def convert_raw_dat_to_phase(data,dims=False):
    
    xps = data['xps']
    eiks = data['eiks']
    Nrays = len(eiks[:,0])
    if not dims:
        Nx=int(np.sqrt(Nrays))
        Ny=Nx;
    else:
        Nx=dims[0];
        Ny=dims[1];
    phase = eiks[:,0] + xps[:,4]*xps[:,0]
    phase -= np.min(phase)
    phase = np.reshape(phase,(Nx,Ny))
    return(phase)


def CalculateFocalLength(basename,wavelength, radius, dims=False,nmax=6):
    phase = extract_phase(basename,dims=dims)
    spectrum = ZernikeSpectrum(phase,nmax=nmax)
    k = 2*np.pi / wavelength;
    focal_length = -k*radius**2/(4*spectrum['c'][4])
    return(focal_length)

def SimpleCalculateFocalLength( spectrum, wavelength=800e-9, radius=1e-3): # units meters
    # Assume spherical phase fronts
    k = 2*np.pi / wavelength;
    focal_length = -k*radius**2/(4*spectrum['c'][4])
    return(focal_length)

def Astigmatism( spectrum, wavelength=800e-9, radius=1e-3): # units meters
    # Use phase front with defocus and astigmatism, find 
    #k = 2*np.pi / wavelength;
    #f = SimpleCalculateFocalLength( spectrum, wavelength=wavelength, radius=radius)
    #a = spectrum['c'][5]
    #b = spectrum['c'][3]
    #mag = np.sqrt(a**2+b**2)
    #L = k*radius**2 / (2*mag)
    #df = 2*(f/L)/(1-(f/L)**2)
    #angle = np.arctan2(-b,a) / 2.0
    #print(angle  * (180/np.pi))
    ##fp = 1.0 / (1/f  +/- 1/L)
    #return(df)
    s2n2 = spectrum['c'][3]
    s20  = spectrum['c'][4]
    s22  = spectrum['c'][5]
    alpha_a = np.sqrt(s22**2+s2n2**2) / s20
    df_over_f = 4*np.abs(alpha_a)/(4+np.abs(alpha_a))
    
    angle = 0.5*np.arctan2(s2n2, s22)             # theta = np.arctan2(y,x)
    print(angle  * (180/np.pi))
    return(df_over_f)




def SphericalAberration( spectrum, wavelength=800e-9, radius=1e-3): # units meters
    # Calculate the Fractional Change in Focal Length due to speherical aberration
    s20 = spectrum['c'][4] # defocus term
    s40 = spectrum['c'][12] # spherical ab term
    ratio = s40/s20;
    df_over_f = -6*ratio/(1-9*ratio**2)
    return(df_over_f)

def show_key_parameters():
    keywords = ["\'number\'", "mks_length =","density_fname"]
    with open(tmppath+'inputs.py') as inF:
        for line in inF:
            for keyword in keywords:
                if keyword in line:
                    print(line)

def extract_files_for_phase(tmppath=None,datpath=None,tarname=None,base='out/test',detector='det1'):
    import tarfile
    import os
    data_types=['eiks','xps']
    prefix = base+'_'+detector
    fnames=[prefix+'_eiks.npy', prefix+'_xps.npy','inputs.py']

    tmppath=os.path.expanduser(tmppath)
    datpath=os.path.expanduser(datpath)
    os.mkdir(tmppath)
    t = tarfile.open(datpath+tarname, 'r')
    for fname in fnames:
        for member in t.getmembers():
            if fname == member.name:
                t.extract(member, tmppath)

    data={}
    for name in data_types:
        data[name]=np.load(tmppath+prefix+'_'+name+'.npy')
        
    clean_files(fnames,tmppath=tmppath)
    return(data, fnames)

def clean_files(fnames,tmppath=None):
    import os
    tmppath=os.path.expanduser(tmppath)
    for fname in fnames:
        os.remove(tmppath+fname)
    os.removedirs(tmppath+'out')
'''
