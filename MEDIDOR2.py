#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import os
import datetime
import csv
import json
import requests

#################################################
fecha = datetime.datetime.now()
fecha = fecha.strftime("%Y-%m-%d")
#################################################
hora = datetime.datetime.now()
hora = hora.strftime("%H:%M:%S")
print("FECHA", fecha)
#DEFINICION DE lectura en valores flotantes
class FloatModbusClient(ModbusClient):
    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None
#CONEXION A PLC Y PUERTO
c = FloatModbusClient(host='192.168.101.99', port=502, auto_open=True)

limite = c.read_input_registers(203, 1)# para leer el reguistro en 16 bits 122,1
device1 = 3    #c.read_input_registers(1, 1)# manual
estado1 = c.read_input_registers(11, 1)#101,1
vrs1 = c.read_float(7, 1)#104,1
vst1 = c.read_float(9, 1)#106,1
vtr1 = c.read_float(11, 1)#108,1
ir1 = c.read_float(13, 1)#110,1
is1 = c.read_float(15, 1)#112,1
it1 = c.read_float(17, 1)#114,1
p_avg1 = c.read_float(2801, 1)#1161
pf_avg = c.read_float(69, 1)#118,1
demand_active = c.read_float(65, 1)#120,1
v_avg_ph_n = 0.0
pfr = 0.0
vtn = 0.0
pfs = 0.0
i_unbal = 0.0
v_avg_ph_ph = 0.0
pft = 0.0
v_unbal = 0.0
vrn = 0.0
vsn = 0.0
######################################
#float_l = c.read_float(202, 9)
print("device:", device1)
print("estado:", estado1)
print("vrs:", vrs1)
print("vst", vst1)
print("VTR", vtr1)
print("IR", ir1)
print("IS", is1)
print("IT", it1)
print("p-avg", p_avg1)
print("PF-avg", pf_avg)
print("demand_active", demand_active)
# TRANSFORMANDO DIC TO LEN
device1 = str(device1).replace('[', '')
device1 = str(device1).replace(']', '')
device1 = int(device1)
estado1 = str(estado1).replace('[', '')
estado1 = str(estado1).replace(']', '')
estado1 = int(estado1)
vst1 = str(vst1).replace('[', '')
vst1 = str(vst1).replace(']', '')
vst1 = str(vst1)
is1 = str(is1).replace('[', '')
is1 = str(is1).replace(']', '')
is1 = str(is1)
ir1 = str(ir1).replace('[', '')
ir1 = str(ir1).replace(']', '')
ir1 = str(ir1)
it1 = str(it1).replace('[', '')
it1 = str(it1).replace(']', '')
it1 = str(it1)
pf_avg = str(pf_avg).replace('[', '')
pf_avg = str(pf_avg).replace(']', '')
pf_avg = str(pf_avg)
demand_active = str(demand_active).replace('[', '')
demand_active = str(demand_active).replace(']', '')
demand_active = str(demand_active)
vtr1 = str(vtr1).replace('[', '')
vtr1 = str(vtr1).replace(']', '')
vtr1 = str(vtr1)
p_avg1 = str(p_avg1).replace('[', '')
p_avg1 = str(p_avg1).replace(']', '')
p_avg1 = str(p_avg1)
vrs1 = str(vrs1).replace('[', '')
vrs1 = str(vrs1).replace(']', '')
vrs1 = str(vrs1)

# TRANSFORMANDO EL ENTERO A BINARIO
print("LIMITE", limite)
salida = str(limite).replace('[', '')
salida1 = str(salida).replace(']', '')
# PROCEDIMIENTO SOLO PARA BINARIO CONSISTE EN QUITAR LOS CORCHETES(DICCIONARIO)
# Y LUEGO PASAR A INT LISTA DE NUMERO NATURALES ENTEROS
salida2 = int(salida1)
salida3 = '{0:016b}'.format(salida2)
print("LIMITE EN BIN", salida3)

# SI SE PIERDE LA CONEXION AL HOST
#192.141.48.55 IP TECNOAPLICA
direccion = "192.141.48.55"
# PING HACIA EL HOST O LA PUERTA DE ENACE
respuesta = os.system("ping -c 3 " + direccion)
#VERIFICACION DE ARCHIVOS EXISTENTES Y CREACION EN CASO NEGATIVO
if os.path.exists("LOG-OK-M2.txt") and os.path.exists("LOG-OK-EXPORT-M2.csv") and os.path.exists("LOG-BKP-M2.txt") and os.path.exists("LOG-BKP-EXPORT-M2.csv"):
    print("estan creados..")
else:
    create_log = open("LOG-OK-M2.txt", "w")
    create_csv = open("LOG-OK-EXPORT-M2.csv", "w")
    create_bkp = open("LOG-BKP-M2.txt", "w")
    create_csv_bkp = open("LOG-BKP-EXPORT-M2.csv", "w")


if respuesta == 0:  # SI RESPONDE EL PING GUARDA LA DATA EN UN ARCHIVO COMO OK Y ENVIA UN PAQUETE JSON
    create_log = open("LOG-OK-M2.txt", "a")
    create_csv = open("LOG-OK-EXPORT-M2.csv", "a")
    reg_lost = str(fecha) + ";" + str(hora) + ";" + str(device1) + ";" + str(estado1) + ";" + str(vrs1) + ";" +\
               str(vst1) + ";" + str(vtr1) + ";" + str(ir1) + ";" + str(is1) +";"+ str(it1)+ ";" + str(p_avg1)+ ";"+ str(pf_avg)+ ";"+\
               str(demand_active)+";" + str(salida3)+";"+str( v_avg_ph_n)+ ";"+str(pfr)+";"+ str(vtn)+ ";" +str(pfs) +\
               ";"+str(i_unbal)+";"+ str(v_avg_ph_ph)+ ";"+ str(pft)+";"+ str(v_unbal)+ ";"+ str(vrn)+";"+str(vsn) + os.linesep
# ELIMINACION-DE-CORCHETE
    eliminar = ('[', ']')
    reg_lost = ''.join(i for i in reg_lost if not i in eliminar)
    create_log.write(reg_lost)
    print("DATA GUARDADA..." + str(reg_lost))
# LEE TXT Y AGREGA A CSV

    data_cvs = open("LOG-OK-M2.txt")
    s = [reg_lost]
    lineas = data_cvs.readlines()
    create_cvs = csv.writer(open("LOG-OK-EXPORT-M2.csv", "a+"), delimiter=';', quoting=csv.QUOTE_ALL)
#ENVIANDO JSON A TECNO APLICA
    create_cvs.writerow(s)
    print("DATOS ESCRITOS EN CSV DIARIO ...")
    url = 'https://www.tecnoaplica.cl/energy/api/v1/measurer/SaveData'
    #url = 'http://192.168.66.241:9000'
    payload = { 'actual': [{"device": device1, "estado": estado1, "vrs": vrs1, "vst": vst1, "vtr": vtr1, "ir": ir1, "is": is1, "it": it1, "p-avg": p_avg1, "pf-avg": pf_avg, "demand-active": demand_active, "limits": salida3,
               "v-avg-ph-n": v_avg_ph_n, "pfr": pfr, "vtn": vtn, "pfs": pfs, "i-unbal": i_unbal, "v-avg-ph-ph": v_avg_ph_ph, "pft": pft, "v-unbal": v_unbal, "vrn": vrn, "vsn": vsn, "fecha": fecha, "hora": hora}]}


    respuesta = requests.post(url, json=payload)
    #respuesta_dict = respuesta.json()

    print("PAYLOAD", payload)
    print("LOG-OK-M2 GUARDADO...")
# SIN RESPUESTA DEL HOST
else:
    create_bkp = open("LOG-BKP-M2.txt", "a")
    reg_lost = str(fecha) + ";" + str(hora) + ";" + str(device1) + ";" + str(estado1) + ";" + str(vrs1) + ";" +\
               str(vst1) +";"+ str(vtr1) +";"+ str(ir1) + ";" + str(is1) +";"+ str(it1)+ ";" + str(p_avg1)+ ";"+ str(pf_avg)+ ";"+\
               str(demand_active)+";"+ str(salida3)+";"+str( v_avg_ph_n)+ ";"+str(pfr)+";"+ str(vtn)+ ";" +str(pfs) +\
               ";"+str(i_unbal)+";"+ str(v_avg_ph_ph)+ ";"+ str(pft)+";"+ str(v_unbal)+ ";"+ str(vrn)+";"+str(vsn) + os.linesep
# ELIMINANDO CORCHETE DEL BKP
    eliminar = ('[', ']')
    reg_losti = ''.join(i for i in reg_lost if not i in eliminar)
    create_bkp.write(reg_losti)
    print("DATA GUARDADA EN LOG-BKP-M2.txt..." + str(reg_losti))
# CREANDO CSV Y POBLANDO EL BKP
    data_csv_bkp = open("LOG-BKP-M2.txt")
    s = [reg_losti]
    lineas = data_csv_bkp.readlines()
    create_cvs = csv.writer(open("LOG-BKP-EXPORT-M2.csv", "a"), delimiter=';', quoting=csv.QUOTE_ALL)
    create_cvs.writerow(s)

    print("DATOS ESCRITOS EN LOG-BKP-EXPORT-M2.csv...")