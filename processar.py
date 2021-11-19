import lags
import os
import pandas as pd
import numpy as np
import netCDF4
import warnings
warnings.filterwarnings("ignore")


dire = 'INMET/'

res = open('resultado.csv','w')
res.write('Ano;Regiao;Estado;Torre;Variavel;Consecutivo;Gap;Outlier;MDQI\n')
res.close()

for root, dirs, files in os.walk(dire, topdown=False):
    print(root)
    dados = []
    for name in files:
        arq = os.path.join(root, name)
        meta = root.split('/')
        ano = meta[-1]
        metadados = arq.split('_')
        regiao = metadados[1]
        estado = metadados[2]
        codtorre = metadados[3]
        torre = metadados[4]
        data = pd.read_csv(arq,sep=';',decimal=',',header = 8)
        x = lags.summary(data.iloc[:,2:])
        a = lags.summary(data.iloc[:,[2,6]], add_consecutive = False)
        x.values[0] = a.values[0]
        x.values[4] = a.values[1]
        x.reset_index(inplace=True)
        initial = [[ano, regiao, estado, torre]]*len(x)
        pInitial = pd.DataFrame(initial)
        l = pd.concat([pInitial,x],axis=1)
        for line in l.values:
            dados.append(list(line))
            
    dados = pd.DataFrame(dados)
    dados.rename(columns={0:'Ano',1:'Regiao',2:'Estado',3:'Torre',4:'Variavel',5:'Consecutivo',6:'Gap',7:'Outlier',8:'MDQI'}, inplace = True)
    dados.to_csv('resultado.csv',sep=';',decimal=',', mode='a', header=False, index=False)
print('FIM')



dire = 'UrbClim/'

res = open('urbclim.csv','w')
res.write('Ano;Mes;MDQI\n')
res.close()

dados = []
for root, dirs, files in os.walk(dire, topdown=False):
    print(root)
    for name in files:
        arq = os.path.join(root, name)
        metadados = arq.split('_')
        ano = metadados[-3]
        mes = metadados[-2]
        f = netCDF4.Dataset(arq,'r')
        temp = f.variables['tas']
        length = temp[:].data.shape
        con = np.reshape(temp[:].data,(length[0],length[1]*length[2])) - 273.15
        data = pd.DataFrame(con)
        x = lags.summary(data, temp[:].fill_value)
        initial = [ano, mes, x.mean()['MDQI']]
        dados.append(initial)
        
dados = pd.DataFrame(dados)
dados.rename(columns={0:'Ano',1:'Mes',2:'MDQI'}, inplace = True)
dados.to_csv('urbclim.csv',sep=';',decimal=',', mode='a', header=False, index=False)
print('FIM')
