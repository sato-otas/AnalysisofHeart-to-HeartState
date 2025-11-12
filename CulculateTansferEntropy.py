import jpype
from jpype import *
import numpy as np
import sys
import pandas as pd
import os


class TEv2_0125():

    Filelist = list()

    #Adapt to your execution environment.
    jarLocation = r"C:\\Users\\sato\\Documents\\JIDT\\infodynamics.jar"
    jvmpath = "C:\\Program Files\\Java\\jdk-25\\bin\\server\\jvm.dll"
    InfodynamicsPath = "C:\\Users\\sato\\Documents\\JIDT"
    
    def __init__(self,datapath,k,l,t,culclist,delaylist)-> None:
        self.datapath = datapath
        self.k = k
        self.l = l
        self.t = t
        self.culclist = culclist
        self.delaylist = delaylist
        
    def getTE(self):

        self.Filelist = os.listdir(os.getcwd()+"\\"+self.datapath)

        resultlist = dict()
        
        for file in self.Filelist:
            data = pd.read_csv(self.datapath+"\\"+file)
            result = list()
            data.reset_index(drop=True, inplace=True)
            data_filled = data.fillna(0)
            array = data_filled.to_numpy()
            for delay in self.delaylist:
                self.Rawresult = [self.TEculc(self.culclist,self.k,self.k,self.t, delay,array[:,:])]
                result.append((self.Rawresult[0][0]+self.Rawresult[0][1])/2)
            result.append(max(result))
            resultlist[file[:-4]] = result
        return resultlist

    def TEculc(self,culclist,k,l,t,delay,data):
        sys.path.append(self.InfodynamicsPath+"\\demos\\python") 
        
        if not jpype.isJVMStarted():
            jpype.startJVM(
                self.jvmpath,
                "-ea",
                "--enable-native-access=ALL-UNNAMED", 
                classpath=[self.jarLocation],
                convertStrings=True
            )

        calcClass = JPackage("infodynamics.measures.continuous.kraskov").TransferEntropyCalculatorKraskov
        calc = calcClass()

        calc.setProperty("k_TAU", str(t))
        calc.setProperty("l_TAU", str(t))
        calc.setProperty("DELAY", str(delay))
        calc.setProperty("NORMALISE", "true")
        calc.setProperty("NOISE_LEVEL_TO_ADD", "0")
        calc.setProperty("k_HISTORY", str(k))
        calc.setProperty("l_HISTORY", str(l))
        calc.setProperty("DELAY", str(delay))

        result_list = list()

        for clist in culclist:
            s = int(clist[0])
            d = int(clist[1])
            res = list()

            data = pd.DataFrame(np.array(data))

            data = np.array(data)
            s
            data[:, s] = pd.to_numeric(data[:, s], errors='coerce')
            data[:, d] = pd.to_numeric(data[:, d], errors='coerce')
            source = JArray(JDouble, 1)(data[:, s].tolist())
            destination = JArray(JDouble, 1)(data[:, d].tolist())

            calc.initialise()
            calc.setObservations(source, destination)
            result_list.append(calc.computeAverageLocalOfObservations())

        return result_list
  
#RtoH
culclistRtoH= [[3,0],[2,1]]

#HtoR
culclistHtoR= [[0,3],[1,2]]

data_path = "Storage"

if __name__ == "__main__":

    k = 100
    l = 100
    t = 2

    #d=[0,5,10,20,30]
    delaylist = [0,5,10,20,30]
    RtoH_cols = ["RtoHd=0", "RtoHd=5", "RtoHd=10", "RtoHd=20", "RtoHd=30",  "RtoHd=Max"]
    HtoR_cols = ["HtoRd=0", "HtoRd=5", "HtoRd=10", "HtoRd=20", "HtoRd=30", "HtoRd=Max"]

    #d=[0,5,10,29]
    # delaylist = [0,5,10,20]
    # RtoH_cols = ["RtoHd=0", "RtoHd=5", "RtoHd=10", "RtoHd=20",  "RtoHd=Max"]
    # HtoR_cols = ["HtoRd=0", "HtoRd=5", "HtoRd=10", "HtoRd=20", "HtoRd=Max"]

    
    TE_RtoH_Instance = TEv2_0125(data_path,k,l,t,culclistRtoH,delaylist)
    RtoH_Result = TE_RtoH_Instance.getTE()

    TE_HtoR_Instance = TEv2_0125(data_path,k,l,t,culclistHtoR,delaylist)
    HtoR_Result = TE_HtoR_Instance.getTE()

    df_Question = pd.read_csv("Questioneer.csv")

    df_Question["ID"] = df_Question["ID"].astype(str)

    df_RtoH = pd.DataFrame.from_dict(RtoH_Result, orient='index', columns=RtoH_cols)
    df_RtoH.index = df_RtoH.index.astype(str)
    df_RtoH.reset_index(inplace=True)
    df_RtoH.rename(columns={'index': 'ID'}, inplace=True)

    df_HtoR = pd.DataFrame.from_dict(HtoR_Result, orient='index', columns=HtoR_cols)
    df_HtoR.index = df_HtoR.index.astype(str)
    df_HtoR.reset_index(inplace=True)
    df_HtoR.rename(columns={'index': 'ID'}, inplace=True)

    df = pd.merge(df_Question, df_RtoH, on='ID', how='left')
    df = pd.merge(df, df_HtoR, on='ID', how='left')

    df.to_csv(f"Result\\datak={k},l={l},t={t},maxdelay={delaylist[-1]}.csv", index=False)



    
