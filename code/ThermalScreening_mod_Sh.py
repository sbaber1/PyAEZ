"""
PyAEZ
Written by N. Lakmal Deshapriya
"""

import numpy as np

class ThermalScreening(object):

    def __init__(self):
        self.set_tclimate_screening = False
        self.set_lgpt_screening = False
        self.set_Tsum_screening = False
        self.set_Tprofile_screening = False


    def getThermalLGP0(self):
        return np.sum(self.meanT_daily>0)

    def getThermalLGP5(self):
        return np.sum(self.meanT_daily>5)

    def getThermalLGP10(self):
        return np.sum(self.meanT_daily>10)

    def getTemperatureSum0(self):
        tempT = self.meanT_daily
        tempT[tempT<=0] = 0
        return np.sum(tempT)

    def getTemperatureSum5(self):
        tempT = self.meanT_daily
        tempT[tempT<=5] = 0
        return np.sum(tempT)

    def getTemperatureSum10(self):
        tempT = self.meanT_daily
        tempT[tempT<=10] = 0
        return np.sum(tempT)

    def getTemperatureProfile(self):

        meanT_daily_add1day = np.concatenate((self.meanT_daily, self.meanT_daily[0:1]))
        meanT_first = meanT_daily_add1day[:-1]
        meanT_diff = meanT_daily_add1day[1:] - meanT_daily_add1day[:-1]

        A9 = np.sum( np.logical_and(meanT_diff>0, meanT_first<-5) )
        A8 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=-5, meanT_first<0)) )
        A7 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=0, meanT_first<5)) )
        A6 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=5, meanT_first<10)) )
        A5 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=10, meanT_first<15)) )
        A4 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=15, meanT_first<20)) )
        A3 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=20, meanT_first<25)) )
        A2 = np.sum( np.logical_and(meanT_diff>0, np.logical_and(meanT_first>=25, meanT_first<30)) )
        A1 = np.sum( np.logical_and(meanT_diff>0, meanT_first>=30) )

        B9 = np.sum( np.logical_and(meanT_diff<0, meanT_first<-5) )
        B8 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=-5, meanT_first<0)) )
        B7 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=0, meanT_first<5)) )
        B6 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=5, meanT_first<10)) )
        B5 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=10, meanT_first<15)) )
        B4 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=15, meanT_first<20)) )
        B3 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=20, meanT_first<25)) )
        B2 = np.sum( np.logical_and(meanT_diff<0, np.logical_and(meanT_first>=25, meanT_first<30)) )
        B1 = np.sum( np.logical_and(meanT_diff<0, meanT_first>=30) )

        return [A9,A8,A7,A6,A5,A4,A3,A2,A1,B1,B2,B3,B4,B5,B6,B7,B8,B9]

    def setClimateData(self, minT_daily, maxT_daily):
        self.meanT_daily = (minT_daily + maxT_daily) / 2

        self.lgp0 = self.getThermalLGP0()
        self.lgp5 = self.getThermalLGP5()
        self.lgp10 = self.getThermalLGP10()

        self.tsum0 = self.getTemperatureSum0()
        self.tsum5 = self.getTemperatureSum5()
        self.tsum10 = self.getTemperatureSum10()

        self.tprofile = self.getTemperatureProfile()

    def setThermalClimateScreening(self, t_climate, no_t_climate):
        self.t_climate = t_climate
        self.no_t_climate = no_t_climate # list of unsuitable thermal climate

        self.set_tclimate_screening = True

    def setLGPTScreening(self, no_lgpt, optm_lgpt):
        self.no_lgpt = no_lgpt
        self.optm_lgpt = optm_lgpt

        self.set_lgpt_screening = True

    # def setTSumScreening(self, no_Tsum, optm_Tsum):
    #     self.no_Tsum = no_Tsum
    #     self.optm_Tsum = optm_Tsum

    #     self.set_Tsum_screening = True

    def SetTSumScreening(self, LnS, LsO, LO, HnS, HsO, HO):
        self.LnS=LnS
        self.LsO=LsO
        self.LO=LO
        self.HnS=HnS
        self.HsO=HsO
        self.HO=HO
        
        self.set_Tsum_screening = True

    
    def setTProfileScreening(self, no_Tprofile, optm_Tprofile):
        self.no_Tprofile = no_Tprofile
        self.optm_Tprofile = optm_Tprofile

        self.set_Tprofile_screening = True


#--------------------------------------------------------------------------------------------------------------------
        """Sriram you can find pesudocode below"""
    def setTypeB('path'):
        #      get formula 
        #      read optimal, sub-opitimal and not suitable data
        #      calculate the values= self.TypeB
        #      self.set_typeBconstraint= true
        #      read the comparsion operator
        #      return calculated values 


        
#-----------------------------------------------------------------------------------------------------------------------------



    def getSuitability(self):

        if self.set_tclimate_screening:
            if self.t_climate in self.no_t_climate:
                return False

        if self.set_lgpt_screening:
            if self.lgp0<=self.no_lgpt[0] or self.lgp5<=self.no_lgpt[1] or self.lgp10<=self.no_lgpt[2]:
                return False
        
        if self.set_Tsum_screening:
            
            # check with thieleng ****
            if (self.tsum0 > self.HnS[0] or self.tsum0 < self.LnS[0]) or (self.tsum5 > self.HnS[1] or self.tsum5 < self.LnS[1]) or (self.tsum10 > self.HnS[2] or self.tsum10 < self.LnS[2]):
                return False

        if self.set_Tprofile_screening:
            for i1 in range(len(self.tprofile)):
                if self.tprofile[i1] <= self.no_Tprofile[i1]:
                    return False

        return True

#------------------------------------------------------------------------------------------------------------------------

        # """Sriram this is for Suitablility test"""
        # for i1 in range(len(self.TypeB))
        # if self.set_TypeBConstrain:
        #     if self.optimal== self.notsuitable:
        #         if self.TypeB comparison_parameter self.optimal:
        #         return False
        #     else:
        #         if self.TypeB comparison_operator self.optimal and self.TypeB comparison_operator self.notsuitable
#-----------------------------------------------------------------------------------------------------------------------


            


    def getReductionFactor(self):

        thermal_screening_f = 1

        # print("reducition applying")
        if self.set_lgpt_screening:

            # fall under typB so will be calcualated in next function

            if self.lgp0 < self.optm_lgpt[0]:
                f1 = ((self.lgp0-self.no_lgpt[0])/(self.optm_lgpt[0]-self.no_lgpt[0])) * 0.75 + 0.25
                thermal_screening_f = np.min([f1,thermal_screening_f])

            if self.lgp5 < self.optm_lgpt[1]:
                f1 = ((self.lgp5-self.no_lgpt[1])/(self.optm_lgpt[1]-self.no_lgpt[1])) * 0.75 + 0.25
                thermal_screening_f = np.min([f1,thermal_screening_f])

            if self.lgp10 < self.optm_lgpt[2]:
                f1 = ((self.lgp10-self.no_lgpt[2])/(self.optm_lgpt[2]-self.no_lgpt[2])) * 0.75 + 0.25
                thermal_screening_f = np.min([f1,thermal_screening_f])
        


        # if self.set_Tsum_screening:

        #     if self.tsum0 < self.optm_Tsum[0]:
        #         f1 = ((self.tsum0-self.no_Tsum[0])/(self.optm_Tsum[0]-self.no_Tsum[0])) * 0.75 + 0.25
        #         thermal_screening_f = np.min([f1,thermal_screening_f])

        #     if self.tsum5 < self.optm_Tsum[1]:
        #         f1 = ((self.tsum5-self.no_Tsum[1])/(self.optm_Tsum[1]-self.no_Tsum[1])) * 0.75 + 0.25
        #         thermal_screening_f = np.min([f1,thermal_screening_f])

        #     if self.tsum10 < self.optm_Tsum[2]:
        #         f1 = ((self.tsum10-self.no_Tsum[2])/(self.optm_Tsum[2]-self.no_Tsum[2])) * 0.75 + 0.25
        #         thermal_screening_f = np.min([f1,thermal_screening_f])
        

        '''the modified reduction factor for T_sum'''
        # print("checking for lololloo ")
        if self.set_Tsum_screening:
            # print("checking for 0, 5, and 10")
            if self.tsum0 > self.LsO[0] and self.tsum0 < self.LO[0] :
                f1 = ((self.tsum0-self.LsO[0])/(self.LO[0]-self.LsO[0])) * 0.25 + 0.75
            elif self.tsum0 > self.HO[0] and self.tsum0 < self.HsO[0]:
                f1 = ((self.tsum0-self.HO[0])/(self.HsO[0]-self.HO[0])) * 0.25 + 0.75
            elif self.tsum0 > self.LnS[0] and self.tsum0 < self.LsO[0]:
                f1 = ((self.tsum0-self.LnS[0])/(self.LsO[0]-self.LnS[0])) * 0.75
            elif self.tsum0 > self.HsO[0] and self.tsum0 < self.HnS[0]:
                f1=((self.tsum0-self.HsO[0])/(self.HnS[0]-self.HsO[0])) * 0.75
            elif self.tsum0 > self.LO[0] and self.tsum0 < self.HO[0]:
                f1 = 1
                # print("im right")

            # confirm with thieleng ***
            thermal_screening_f = np.min([f1,thermal_screening_f])
            
            if self.tsum5 > self.LsO[1] and self.tsum5 < self.LO[1] :
                f1 = ((self.tsum5-self.LsO[1])/(self.LO[1]-self.LsO[1])) * 0.25 + 0.75
            elif self.tsum5 > self.LnS[1] and self.tsum5 < self.LsO[1]:
                f1=((self.tsum5-self.LnS[1])/(self.LsO[1]-self.LnS[1])) * 0.75
            elif self.tsum5 > self.HO[1] and self.Tsum5 < self.HsO[1]:
                f1 = ((self.tsum5-self.HO[1])/(self.HsO[1]-self.HO[1])) * 0.25 + 0.75
            elif self.tsum5 > self.HsO[1] and self.tsum5 < self.HnS[1]:
                f1=((self.tsum5-self.HsO[1])/(self.HnS[1]-self.HsO[1])) * 0.75

            # confirm with thieleng ***
            thermal_screening_f = np.min([f1,thermal_screening_f])

            if self.tsum10 > self.LsO[2] and self.tsum10 < self.LO[2] :
                f1 = ((self.tsum10-self.LsO[2])/(self.LO[2]-self.LsO[2])) * 0.25 + 0.75
            elif self.tsum10 > self.LnS[2] and self.tsum10 < self.LsO[2]:
                f1=((self.tsum0-self.LnS[2])/(self.LsO[2]-self.LnS[2])) * 0.75
            elif self.tsum10 > self.HO[2] and self.Tsum10 < self.HsO[2]:
                f1 = ((self.tsum10-self.HO[2])/(self.HsO[2]-self.HO[2])) * 0.25 + 0.75
            elif self.tsum10 > self.HsO[2] and self.tsum10 < self.HnS[2]:
                f1=((self.tsum10-self.HsO[2])/(self.HnS[2]-self.HsO[2])) * 0.75
        
            # confirm with thieleng ***
            thermal_screening_f = np.min([f1,thermal_screening_f])        

        if self.set_Tprofile_screening:

            for i1 in range(len(tprofile)):
                if self.tprofile[i1] < self.optm_Tprofile[i1]:
                    f1 = ((self.tprofile[i1]-self.no_Tprofile[i1])/(self.optm_Tprofile[i1]-self.no_Tprofile[i1])) * 0.75 + 0.25
                    thermal_screening_f = np.min([f1,thermal_screening_f])

        return thermal_screening_f

        def getsuitability_typeB():
            read csv file 
            if self.set_TypeB:
                for i1 in range(len(self.typeB)):
                    if self.optimal[i1]==self.notsuitable[i1]:
                        f1= 1
                    elif self.optimal[i1] != self.suboptimal[i1] and self.subopitmal[i1] != self.notsuitable[i1]:
                        if self.TypeB[i1] comparison_paramer self.optimal[i1] and self.TypeB[i1] comparison parameter self. sub0ptimal[i1]:
                            f1 = ((self.TypeB-self.LsO[i1])/(self.LO[2]-self.LsO[2])) * 0.25 + 0.75





                set 


