from math import factorial
import scipy as sp
from scipy import absolute as abs
import matplotlib.pylab as plt
#from copy import deepcopy

def neumann_factor(m):
    if m==0:
        return(2)
    else:
        return(1)


def osa_index(n,m):
    """
    Calculates the OSA j-index.
    
    :param n: non-negative radial index
    :param m: azimuthal index 
    :returns: the j-index
    """
    j = (n*(n+2)+m)/2
    return(j)

def unitsquare(resolution,coord='xy'):
    """
    Create a 2D arrays for x,y coordinates in unit square
    """    
    x = sp.linspace(-1,1,resolution)
    y = sp.linspace(-1,1,resolution)
    X,Y = sp.meshgrid(x,y)
    if coord=='xy':
        return(X,Y)
    elif coord=='rphi':
        R = sp.sqrt(X**2+Y**2);
        PHI = sp.arctan2(Y,X)
        return(R,PHI)


def radial_zernike(rho,n,m,outside=0.0):
    R = sp.zeros_like(rho)
    m=abs(m); #sign of m does not change radial function
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

def angular_zernike(phi,m):
    phase = abs(m) * phi;
    if m<0: # negative
        return(sp.sin(phase))
    else:   # non-negative
        return(sp.cos(phase))
    
def Zernike(rho,phi,n,m,outside=0):
     return(RadialZernike(rho,n,m,outside=outside)*AngularZernike(phi,m))
    
def CalculateZernikeCoefficient(phase,n,m,debug=False):    
    Phase = phase.copy() 
    Nx, Ny = sp.shape(Phase)
    if debug: print("Dims of phase: ",Nx,Ny)
    if Nx==Ny:
        Resolution=Nx
    else:
        abort()
    if (n-m) % 2 == 0: # is even?
        
        x = sp.linspace(-1,1,Resolution);
        y = sp.linspace(-1,1,Resolution);
        dx=x[1]-x[0]; 
        dy=y[1]-y[0];
        if debug: print('dx,dy =',dx,dy)
        X,Y = sp.meshgrid(x,y)
        R = sp.sqrt(X**2+Y**2);
        phi = sp.arctan2(Y,X)
        top = 2*n+2
        bot = neumann_factor(m)*sp.pi
        if debug: print('top =',top)
        if debug: print('bot =',bot)
        Phase[R>1] = 0.0
        if debug: print('max phase =',sp.max(Phase))       
        if debug: print('min phase =',sp.min(Phase))  
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
            
        amn=(top/bot)*sp.sum(Phase * Zernike(R,phi,n,m,outside=0)*dx*dy)
        return(amn)
    else:
        return(0.0)

    
def ZernikeSpectrum(Phase,nmax=6,Symmetry=None):
    spectrum={}
    spectrum['c']=sp.array([])      # coefficient
    spectrum['j']=sp.array([])       # OSA Index
    spectrum['n']=sp.array([])       # Radial Index
    spectrum['m']=sp.array([])       # Angular Index

    for n in range(nmax+1): # go up to nmax
        for m in range(-n,n+1): #range from -n to n
            if (n-m) % 2 == 0: # is even?
                #print(OSAindex(n,m),n,m,amn)
                spectrum['j'] = sp.append(spectrum['j'],int(OSAindex(n,m)))
                spectrum['n'] = sp.append(spectrum['n'],int(n))
                spectrum['m'] = sp.append(spectrum['m'],int(m))
                if Symmetry==None:
                    spectrum['c'] = sp.append(spectrum['c'],CalculateZernikeCoefficient(Phase,n,m))
                if Symmetry=='Azimuthal':
                    if m==0:
                        spectrum['c'] = sp.append(spectrum['c'],CalculateZernikeCoefficient(Phase,n,m))
                    else:
                        spectrum['c'] = sp.append(spectrum['c'],0.0)

                    



    return(spectrum)


def PlotZernikeSpecturm(Spectrum,IncludePiston=False,unit='rad',PlotThreshold=1e-14,Symmetry=None):
    show_element = sp.absolute(Spectrum['c']) >= PlotThreshold
    
    if Symmetry =='Azimuthal':
        show_element[Spectrum['m']!=0]=False
    
    if IncludePiston:
        show_element[0]=True
    else:
        show_element[0]=False

    if Symmetry=='Azimuthal':
        j=(Spectrum['n'][show_element]).copy()
    else:
        j = (Spectrum['j'][show_element]).copy()
    c = Spectrum['c'][show_element]
        
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(4,3)
    ax.plot(j,c,'.k')

    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    #ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    if IncludePiston:   xticks = sp.arange(0,j[-1],1)
    else:               xticks = sp.arange(1,j[-1],1)
    ax.set_xticks(xticks,minor=True)
    
    ymax = sp.nanmax(sp.absolute(c))
    plt.ylim(-1.1*ymax,1.1*ymax)
    
    if not unit=='':
        ax.set_ylabel('Zernike Coefficient ('+unit+')')
    else:
        ax.set_ylabel('Zernike Coefficient')
    if Symmetry=='Azimuthal':
        ax.set_xlabel('$n$, radial index')
    else:
        ax.set_xlabel('$j$, OSA Index')
    return(fig,ax)

def reconstruct(s,resolution):
    phase = sp.zeros((resolution,resolution));
    R, PHI = unitsquare(resolution,coord='rphi')
    for j,n,m in zip(s['j'],s['n'],s['m']):
        phase += s['c'][int(j)]*Zernike(R,PHI,n,m,outside=0)
    return(phase)



def SimpleCalculateFocalLength( spectrum, wavelength=800e-9, radius=1e-3): # units meters
    '''
    Calculate focal length assuming spherical phase fronts
        
    spectrum 
    wavelength  units in meters
    radius      radius of lens in meters
    '''
    # Assume spherical phase fronts
    k = 2*sp.pi / wavelength;
    focal_length = -k*radius**2/(4*spectrum['c'][4])
    return(focal_length)


OSAindex=osa_index
RadialZernike=radial_zernike
AngularZernike=angular_zernike    
