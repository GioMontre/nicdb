"""
    Author: Giovanni Montresor
"""
import os
from icecream import ic
import utility.log as l
import sqlite3


def main():
    con = sqlite3.connect("../data/nic.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE t_Netadaptconf(caption, IP, MAC, tstamp)")


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