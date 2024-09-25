"""
    Author: Giovanni Montresor
"""
import time
import wmi
import utility.log as l
import os
from icecream import ic
import platform
import csv


def get_nics(machine):
    nics = []
    c = wmi.WMI(f"{machine}")

    for nic in c.Win32_NetworkAdapterConfiguration():
        if nic.IPAddress:
            ic(nic.Description, nic.MACAddress, nic.IPAddress)
            nics.append(nic)
    return nics


def save_nics(nics: list):

    epoch_time = str(time.time())[0:13]
    uname = platform.uname().node

    with open(f"../flussi/{epoch_time}_{uname}.csv", "w", encoding='UTF8', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(["caption", "IP", "MAC", "tstamp"])

        for nic in nics:
            caption = nic.Caption  # Nome della scheda di rete
            ip = nic.IPAddress  # Indirizzo IP
            mac = nic.MACAddress  # Indirizzo MAC
            tstamp = epoch_time

            writer.writerow([caption, ip, mac, tstamp])

        logs.write_msg("salvataggio nel csv")

    with open(f"../flussi/{epoch_time}_{uname}.sql", "w", encoding='UTF8', newline='') as file_sql:
        for nic in nics:
            file_sql.write(f"INSERT INTO t_Netadaptconf (caption, IP, MAC, tstamp) VALUES ('{nic.Caption}', '{nic.IPAddress}', '{nic.MACAddress}', '{epoch_time}')\n")

        logs.write_msg("crezione comandi per tabella sql")


def main():
    nics = get_nics(".")
    ic(nics)
    logs.write_msg("nic ricavate")

    save_nics(nics)



if __name__ == '__main__':
    nome_f = os.path.basename(__file__)
    logs = l.Log(nome_f)
    logs.log(False)

    try:
        main()
    except Exception as er:
        ic("Error", er)
        logs.write_error(f"{er}")

    logs.log(True)
