from pprint import pprint

class Occupant(object):
    def __init__(self):
        self.room = 0 # id of room occupied, time dependent
        self.preference = {
            'temperature': 24,
            'humidity': .3
        }
        self.comfort = 1.0
        return

    def calculateComfort(self, room):
        # 6 primary factors for thermal comfort per ASHRAE 55
        # 1. metabolic rate
        #       seated, sedentary 1.0 to 1.3 met
        #       sleeping 0.7 met
        #       1 met = 58.2 W/m^2
        #       chemical energy converted to heat
        #       expressed per surface area of avg person seated at rest
        #       avg surface area = 1.8 m^2
        #       to calculate surface area,  A_D=0.108*m^0.425*l^0.725
        #       A_D DuBois surface area ft^2, m weight lb, l height inches
        # 2. clothing insulation
        #       typ 0.5 to 1.0
        #       1 clo = 0.155 m^2*C/W
        # 3. air temperature
        # 4. radiant temperature
        # 5. air speed
        # 6. humidity
        comfort = 0.0

        #meanRadiantTemperature = math.pow(math.fsum(0.25*wall.temperature for wall in room.walls), 0.25)
        # simplification, use the bulk room temperature
        meanRadiantTemperature = room.temperature

        return comfort

    def calculatePMVPPD(self):
        #Calculates PMV and PPD Based on I S O Standard 7730
        Conditions = {
            'MRT': 24.0,
            'AirVelocity': 0.15,
            'AirVelocityCorrection': False,
            'Met': 1.0,
            'ExternalWork': 0.0,
            'Clo': 0.5
        }
        pprint(Conditions)
        ICL = 0.0
        METFACTOR = 1.0
        AirVelocity = Conditions['AirVelocity']

        #Optional Air Velocity Correction for Met > 1
        if (Conditions['AirVelocityCorrection'] and Conditions['Met']>1):
            AirVelocity = AirVelocity + 0.3*(Conditions['Met']-1)

        AirVelocity = max(AirVelocity, 0.1)
        PressureInPascals = CalcVaporPressure() * 1000
        ICL = .155 * Conditions['Clo']
        M = Conditions['Met'] * METFACTOR
        W = Conditions['ExternalWork'] * METFACTOR
        Tolerance = .00015
        MW = M - W

        # Compute the corresponding FCL value
        if (ICL < .078):
            FCL = 1.0 + 1.29 * ICL
        else:
            FCL = 1.05 + .645 * ICL

        FCIC = ICL * FCL
        P2 = FCIC*3.96
        P3 = FCIC*100.0
        TRA = Conditions.MRT+273.0
        TAA = Conditions['AirTemperature'] + 273.0
        P1 = FCIC * TAA
        P4 = 308.7 - 0.028 * MW + P2 * math.pow(TRA/100.0, 4)

        #First guess for surface temperature
        TCLA = TAA + (35.5-Conditions['AirTemperature']) / (3.5*(6.45*ICL+0.1))
        XN = TCLA / 100.0
        XF = XN
        HCF=12.1*math.sqrt(AirVelocity)
        nIterations=0

        #COMPUTE SUFACE TEMPERATURE OF CLOTHING BY ITERATIONS
        while (nIterations < 150):
            XF=(XF+XN)/2.0
            HCN=2.38*math.pow(math.abs(100*XF-TAA),.25)
            if (HCF>HCN):
                HC=HCF
            else:
                HC=HCN
            XN=(P4+P1*HC-P2*math.pow(XF,4))/(100.0+P3*HC)
            nIterations = nIterations + 1
            if (nIterations>1 and math.abs(XN-XF)<=Tolerance):
                break
            TCL = 100.0*XN - 273.0
        #end while

        #COMPUTE PMV
        if (nIterations < 150):
            #don//t do it if we didn//t find clothing temperature
            PM1=3.96*FCL*(math.pow(XN,4)-math.pow((TRA/100.0),4))
            PM2 = FCL * HC * (TCL-Conditions['AirTemperature'])
            PM3 = .303 * math.exp(-.036*M) + .028
            if (MW > OneMet):
                PM4 = .42 * (MW-OneMet)
            else:
                PM4 = 0.0

            PM5 = 3.05*.001*(5733.0-6.99*MW-PressureInPascals)
            PM6 = 1.7 * .00001 * M * (5867.0-PressureInPascals) + .0014 * M * (34.0-Conditions['AirTemperature'])

            PMV = PM3 * (MW-PM5-PM4-PM6-PM1-PM2)
            TCLN = (TCL*100.0)/100.0
            #Compute PPD
            PPD = 0.01*(100.0 - 95.0*math.exp(-.03353*math.pow(PMV,4)- 0.2179*math.pow(PMV,2)))
        else:
            return -1

        return [PMV, PPD]

if __name__ == '__main__':
    oc = Occupant()
