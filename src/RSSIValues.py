from subprocess import Popen, PIPE
import pandas as pd
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt
NETWORKS=['mlatAlpha','mlatBravo','mlatC','mlatDelta']
FREQUENCY=5200
def main():
    asd = networkScan("wlp1s0")
    # logRssi(networks,number of logs, time between logs in seconds)


    log, times = asd.logRssi(NETWORKS, 5,10)
    dlog=log
    for i in log:
        for j in range(len(log[i])):
            dlog[i][j]=distance(log[i][j])
    print(dlog)
    df = pd.DataFrame(dlog, index=times)



    df.to_csv("test.csv")

"""    fig, ax = plt.subplots()
    ax.plot(times,dlog, label='mlatAlpha')
    plt.xlabel("time")
    plt.ylabel("meters")
    plt.title("15 second increments")
    #ax.plot(times,log['mlatBravo'], label='mlatBravo')
    #ax.plot(times,log['mlatC'], label='mlatC')
    #ax.plot(times,log['mlatDelta'], label='mlatDelta')
    #ax.legend()
    plt.show()
"""

def distance(RSSI):
    distance = 10 ** ((27.55 - (20 * np.log10(FREQUENCY)) + np.abs(RSSI)) / 20)
    return distance




class networkScan():
    def __init__(self, interface):
        self.interface = interface

    # This function passes a command that lists off all of the wifi connections and their properties
    # and returns it
    # interface reefers to the type of connection, ie wlp1s0
    def getNetworks(self):
        scanCommand = ["sudo", "iw", "dev", self.interface, "scan"]
        networkInfo = Popen(scanCommand, stdout=PIPE,stderr=PIPE)
        (raw_output, raw_error) = networkInfo.communicate()
        raw_output = raw_output.decode("utf-8")
        return [raw_output, str(raw_error)]

    # gets the networks SSID
    @staticmethod
    def getSSID(raw_cell):
        # grabs the string after 'ssid:' and then splits it at every ' '
        ssid = raw_cell.split('SSID:')[1]
        ssid = ssid.split()[0]
        return ssid

    # gets the signal level
    @staticmethod
    def getSignalLevel(raw_cell):
        # grabs the string after 'signal: ' and then splits it at every ' '
        rssi = raw_cell.split('signal: ')[1]
        rssi = float(rssi.split()[0])
        return rssi

    # gathers the data that we care about and puts it into a dictionary called cell
    def parseCell(self, raw_cell):
        cell = {
            'ssid': self.getSSID(raw_cell),
            'signal': self.getSignalLevel(raw_cell)
        }
        return cell

    # creates an array containing the information that we care about for each network
    def networkCells(self):
        raw_output, raw_error = self.getNetworks()
        # we split at wlp1so because it only appears once per network in the raw output
        raw_cells = raw_output.split('wlp1s0')
        # remove everything before the first instance of 'wlp1s0' becuase there is no useful information there
        # and therefore cant be parsed
        raw_cells.pop(0)
        network_cells = []
        for cell in raw_cells:
            network_cells.append(self.parseCell(cell))
        return network_cells

    # removes cells for networks that we do not care about
    def wantedNetworks(self, networks):
        wanted_network_cells = []
        for cell in self.networkCells():
            if cell['ssid'] in networks:

                wanted_network_cells.append(cell)
        print(wanted_network_cells)
        return wanted_network_cells

    def distances(self):


        pass

    # logs rss values into a dictionary with the format of {'ssid':[x,y,z]} where x,y, and z are rssi values
    def logRssi(self, networks, measures, delay):
        rss_log = {}
        current_time = 0
        times = []

        # sets up the dictionary for every network
        for i in networks:
            rss_log.update({i: []})

        # logs all rss values for the amount of measures chosen
        for i in range(measures):
            startTime = time()
            cells = self.wantedNetworks(networks)
            for j in range(len(networks)):
                values = rss_log[networks[j]]
                values.append(int(cells[j]['signal']))
                rss_log.update({networks[j]: values})
            sleep(delay)
            stopTime = time()
            totalTime = stopTime - startTime
            # logs the time for each measurement taken
            current_time += totalTime
            times.append(current_time)
            print(i)
        return (rss_log, times)


main()
