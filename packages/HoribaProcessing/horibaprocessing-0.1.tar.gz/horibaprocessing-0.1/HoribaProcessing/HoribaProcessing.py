class HoribaProcessor:
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
    
    def __init__(self,peakStart=None, peakStop=None, averaging=False, fileType=".xlsx", flatten=False, polyOrder=3, peakSelector=True, intro=True):
        if intro:
            print( """
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
             """)
        #List of definitions to use in the class
        
        self.averaging = averaging #Class parameter to average the given spectra >> storeData(), flattenSpectra()
        self.fileType = fileType # Class parameter to set the given filetype (.xlsx or .csv) CURRENTLY ONLY SUPPORTS .XLSX >> readFiles()
        self.peakStart = peakStart # Class parameter to determine the start of the peak of interest >> flattenSpectra()
        self.peakStop = peakStop # Class paramter to determine the end of the peak op interest >> flattenSpectra()
        self.polyOrder = polyOrder # Class parameter to determinde the order of polynomial to do background fitting >> flattenSpectra() 
        self.peakSelector = peakSelector # Class parameter to determine which peak needs to be analyzed >> peakSelector()
        self.flatten = flatten # Class paramter to determine of the spectra need to be flattened (Remove background around peak) >> returnFlatSpectra()
        self.libraryImport() # Calls function to import libraries and modules
        if peakStart or peakStop is not None and peakSelector is True:
            print(colored("Warning: peakStart and peakStop parameters overriden by peakSelector being True. Set class parameter peakSelector to False to manually select peaks",'red','on_yellow', attrs=['bold', 'underline']))
        self.listFiles() # Calls function to list files in current directory 
        self.readFiles() # Calls function to read files in current directory ending in "self.fileType"
        self.importJson() # Calls funtion to get list of molecules with cm^-1 parameter from json file 
        

    def libraryImport(self):
        """
        Function to import libraries used inside and outside of class
        
        Function is always called automatically in class
        """
        #Global identifiers to use imports inside and outside class
        global np
        global plt
        global pd
        global os
        global xlrd
        global Polynomial 
        global sys
        global json
        global sp
        global colored
        
        #Importing different libraries and modules
        import numpy as np # Numpy for calculations and array manipulation
        import matplotlib.pyplot as plt # matplotlib for use in plotting different graphs and spectra
        import pandas as pd # Pandas used for importing files into python
        import os as os # os used for getting list of files in CWD
        from numpy.polynomial import Polynomial as Polynomial # numpy.Polynomial is used to fit the background of the peaks.
        import sys # used for handling exceptions
        import json as json # Used to locate peaks 
        import scipy as sp # 
        from termcolor import colored # Used for coloured text

    
    


    def importJson(self):
        f = open("database.json", 'r')
        database = json.loads(f.read())
        self.database = database['Molecules']
        
    def moleculeSelector(self):
        molecule = None
        question = "The above molecules are registered. Please pick one. \n"
        for i in self.database:
            print(i)
        selected_molecule = input(question)
        if selected_molecule.upper() not in self.database:
            sys.exit("Selected molecule %s not in database" % selected_molecule.upper())
        else: 
            molecule = selected_molecule.upper()
            print("Molecule %s has been selected" % selected_molecule.upper())
        self.molecule = molecule
        
    def peakFinder(self):
        moleculePixel = round((self.database[self.molecule]+360.99)/2.578539)
        self.peakStart = moleculePixel-30
        self.peakStop = moleculePixel+30
        
    
    def listFiles(self): # Function to list files in CWD. Creates list with all files in CWD (Excluding calibration file, which is sent to a different variable) 
        """
        Function to list all the files in the Current Working Directory (CWD)
        
        Uses: self.fileType (String)
        
        Returns: fileList (List)
        
        Function is always called automatically in class
        """
        filelist = [] # Empty list to fill with filenames
        calibration = None
        for file in os.listdir(os.getcwd()): # Check for files in the current directory
            if file.endswith(self.fileType): # Check for correct filetype
                if file != "calibration.xlsx": # Exclude calibration file
                    filelist.append(file) # Add correct file to filelist
                else:
                    calibration = file
        self.calibration = calibration
        self.fileList = filelist # Make variable usable class-wide

    


    def readFiles(self):
        """
        Function to read the files in self.fileList
        
        Uses: self.fileType (String), self.fileList (List)
        
        Outputs: self.fileDict (Dictionary)
        
        Function is always called automatically in class
        """
        
        fileDict = {} # Empty dictionary to fill with file data
        for i in self.fileList: # for every element in self.fileList
            fileData = {} # Dummy storage for file data
            
            if self.fileType == ".xlsx":  # Identifier for filetype: xlsx
                openFile = pd.read_excel(i,sheet_name=1).to_numpy() # Open file via pandas, convert to numpy array 
                fileData["dateTime"] = openFile[0][1] # Add date and time to fileData
                fileData["ExposureTime"] = openFile[1][1] # Add used exposure time to fileData
                fileData["timeUnit"] = openFile[3][1] # Add unit of time used to fileData
                fileData["scanSpeed"] = openFile[4][1] # Add readout speed used to fileData
                fileData["gain"] = openFile[5][1] # Add gain used to fileData
                fileData["spectra"] = openFile[10:].transpose()[2:] # Add list of recorded spectra in file to fileData
            
            elif self.fileType == ".csv": # Identifier for filetype: csv
                print("Nog niet afgemaakt") # If filetype csv is selected, return print for work in progress
            fileDict[i] = fileData # Store fileData in fileDict to move onto next file
        self.fileDict = fileDict # Make variable usable class-wide
      
        if self.peakSelector:
            self.importJson()
            self.moleculeSelector()
            self.peakFinder()
      
    
    def storeData(self): # Function to return spectra from fileDict into usable format. 
        """
        Function to return the spectra stored in self.fileDict into a usable format
        
        Uses: self.averaging (Bool), self.fileDict (Dictionary)
        
        Outputs: dummyData (Dictionary)
        
        Function is called in returnData()
        """
        
        dummyData = {} # dictionary to be returned
        if self.averaging: # Check for averaging
            for i in self.fileDict: # for each element/file in fileDict
                dummyData[i]=(np.average(self.fileDict[i]["spectra"],axis=0)) # Add filename with averaged spectra to dummyData
        else: # Not averaging
            for i in self.fileDict: # for each element.file in fileDict 
                dummyData[i]=(self.fileDict[i]["spectra"]) # Add filename with spectra to dummyData
        return dummyData # return the filename with spectra in a dictionary
    
    def flattenSpectra(self, spectra): # Function to flatten spectra around peak. 
        """
        Function to flatten the background around a peak. Used to compare a peaks between different spectra regardless of background.
        
        Uses: spectra (list), self.peakStart (Integer), self.peakStop (Integer), self.polyOrder (Integer), self.averaging (Boolean)
        
        self.peakStart and self.peakStop have to be handpicked to fit the entire peak that needs to be flattened. polyOrder is set to 3 as standard, can be changed in class setup
        
        Outputs: spectra_removed_bg (List)
        
        Function is called in returnFlatSpectra
        """
        if self.averaging: # Check for averaging
            spectraL = spectra[(self.peakStart-100):(self.peakStop+100)] # Isolate peak from spectrum
            dummyX = np.arange(0,len(spectraL),1) # Make a dummy list for eventual fit
            x_filter = np.concatenate((np.arange(0,100,1),np.arange(100+(self.peakStop-self.peakStart),len(spectraL),1))) # Create x-axis list for filtered spectra
            spectra_filter = np.concatenate((spectraL[0:100],spectraL[(100+(self.peakStop-self.peakStart)):len(spectraL)])) # Filter peak from spectra for background fit
            poly = Polynomial.fit(x_filter.astype('float'),spectra_filter.astype('float'),self.polyOrder) # Fit polynomial with order: self.polyOrder to background
            spectra_removed_bg = spectraL-poly(dummyX) # Remove fitted background from isolated peak region
            self.spectra_removed_bg = spectra_removed_bg # Make variable available class-wide
            return spectra_removed_bg # Return flattened spectra 
        
        elif not self.averaging: # check for averaging
            spectraL = [] # Setup list with isolated peaks
            spectra_filter = [] # Setup list for peak filtered spectra
            bgPoly = []  # Setup list for background polynomial
            spectra_removed_bg = [] # Setup list for isolated peak with removed background
            for i in spectra.transpose(): # For each element in list of spectra 
                spectraL.append(i[(self.peakStart-100):(self.peakStop+100)]) # Append isolated peak region to spectraL
            for i in spectraL: # For each isolated peak in spectraL 
                dummyX = np.arange(0,len(i),1) # Arange dummy list
                spectra_filter.append(np.concatenate((i[0:100],i[(100+(self.peakStop-self.peakStart)):len(i)]))) # Filter peak from spectra and add to spectra_filter
                x_filter = np.concatenate((np.arange(0,100,1),np.arange(100+(self.peakStop-self.peakStart),len(i),1))) # Setup new x-axis
            for i in spectra_filter: # For each peak filtered spectra in spectra_filter
                poly = Polynomial.fit(x_filter,i,self.polyOrder) # Fit self.polyOrder order polynomial to background
                bgPoly.append(poly(dummyX)) # Create list of polynomial values
            spectra_removed_bg = (np.array(spectraL)-np.array(bgPoly)).transpose() # remove polynomial list from isolated peak to flatten 
            self.spectra_removed_bg = spectra_removed_bg # Make variable available class-wide
            return spectra_removed_bg # Return flattened spectra 
            
    
    
    
    def returnFiles(self):
        """
        Function to return a list of read files in CWD.
        
        Uses: self.fileList (List)
        
        Outputs: self.fileList (List)
        
        Function to be called outside of class to return list of used files
        """
        
        return self.fileList # returns variable fileList (Type: List) 
    
   
    
    def returnRawData(self):
        """
        Function to return a dictionary with data from all read files
        
        Uses: self.fileDict (Dictionary)
        
        Outputs: self.fileDict (Dictionary)
        
        Function to be called outside of class to return dictionary with all file information
        """
        return self.fileDict
    
    def returnData(self): # Function to return only spectra from files (Type: Dictionary)
        """
        Function to return only the spectra attached to a filename
        
        Uses: self.storeData (Dictionary)
        
        Outputs: self.storeData (Dictionary)
        
        Function to be called outside of class to return dictionary of filenames with spectra 
        """
        return self.storeData()
          
        
        
    def returnFlatSpectra(self):
        """
        Function to return flattened spectra attached to a filename
        
        Uses: flattenSpectra() (Function), self.fileDict (Dictionary), storeData() (Function)
        
        Outputs: flat_spectra (dictionary)
        
        Function to be called outside of class to return dictionary of files with flattened spectra. 
        """
        
        flat_spectra = {} # Dictionary to store flattened spectra with filename
        for i in self.fileDict: # For each element/file in self.fileDict
            try:
                flat_spectra[i] = self.flattenSpectra(self.storeData()[i]) # Add flattened spectra to flat_spectra
            except TypeError:
                sys.exit("Set an integer value for peakStart and peakStop. See class documentation")
        self.flat_spectra = flat_spectra # Make variable available class-wide
        return flat_spectra # return the flat_spectra dictionary
    
HP = HoribaProcessor(flatten=True, averaging=True, polyOrder=2, peakSelector=True)
data = HP.returnFlatSpectra()
files = HP.returnFiles()
rawData = HP.returnRawData()
plt.plot(data[files[0]])
