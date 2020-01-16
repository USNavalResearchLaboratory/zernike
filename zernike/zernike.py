

'''

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

'''


'''

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


