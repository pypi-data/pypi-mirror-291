"""
    This class is made to process spectra produced form the Horiba camera using the provided software for the camera. 
    
    The class needs to be initialized with the following parameters:
        -peakstart: Integer. Tells the class where to look for the start of a peak. Has to be set by hand (for now)
        -peakStop: Integer. Tells the class where to look for the end of a peak. Has t obe set by hand (for now)
        -averaging: Boolean (standard=False) # Tells the class to average the spectra or work with every raw spectrum
        -fileType: String (standard=.xlsx) # Tells the class which filetype to look for and read
        -flatten: Boolean (standard=False) # Tells the class whether to flatten the spectra from the files
        -polyOrder: Integer (standard=3) # Tells the class what order polynomial to use for background fitting of peaks
        -locatePeak: Boolean (standard=True) # Tells the class to locate a peak (Only on spectra after 19/08/24) CHANGES TO OPTICAL SETUP REQUIRE NEW CALIBRATION FILE. OVERRIDES PEAKSTOP AND PEAKSTART!
        
    Callable functions of class:
        -returnFiles(self) ->  returns list of all files in CWD
        -returnRawData(self) -> returns dictionary with files as keys containing all information from files
        -returnData(self) -> returns dictionary with files as keys containing spectra from files
        -returnFlatSpectra(self) -> returns dictionary with files as keys containing flattened spectra from isolated peak
        
    
    Class made by Rico Koster (R&D Engineer @ Hobré Instruments Purmerend. 19/08/24)
    For contact and questions please email r.koster@hobre.com
    """