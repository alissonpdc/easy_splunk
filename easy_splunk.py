##########################################################################
#                                                                        #
#    MODULO PYTHON PARA EXPORTACAO DE DADOS VIA JSON PARA SPLUNK ITAU    # 
#    EXECUCAO VIA THREAD PARA PARALELISTMO                               #
#                                                                        #
#    ALISSON PRADO DA CRUZ                                               #
#    MAIO / 2019                                                         #
#                                                                        #
##########################################################################


import requests
import json
from multiprocessing import Process


class Splunk():
    '''
    DOCSTRING: Funcao para abstracao do envio de dados em formato json para o Splunk Itau
    INPUT: string ambiente ("prod"/"dev"/"shadow")
           int timeout
    OUTPUT: apenas em caso de erro
    '''
    def __init__(self,ambiente,timeout=30):
        if(ambiente.lower() == 'prod'):
            self.url = 'https://172.31.25.55:8088'
            self.key = '29A2070B-4D03-4695-8BC9-D332D7B71B64'
        elif(ambiente.lower() == 'dev'):
            self.url = 'https://10.56.156.65:8088'
            self.key = '4da23032-3be2-4435-9be3-e93db3652415'
        elif(ambiente.lower() == 'shadow'):
            self.url = 'http://10.54.39.199:8088'
            self.key = 'e386f95c-97d1-4bcb-b884-313167c3bf11'
        elif(ambiente.lower() == 'teste'):
            self.url = 'http://testeee.itau'
            self.key = 'e386f95c-97d1-4bcb-b884-313167c3bf11'
        else:
            raise ValueError("O parametro 'ambiente' deve ser: 'prod', 'dev' ou 'shadow' (informado '"+ambiente+"'")
                
        self.timeout = timeout
        self.ambiente = ambiente
        self.headers = {'Authorization': 'Splunk '+self.key}
        self.export_url = self.url+'/services/collector/event'

        
    def __str__(self):
        '''
        Funcao para print() das variaveis do objeto Splunk
        OUTPUT: string url
                string ambiente
                string hec-key
        '''
        splunk_info = {}
        splunk_info['url'] = self.url
        splunk_info['ambiente'] = self.ambiente
        splunk_info['key'] = self.key
        return str(splunk_info)

    def _export(self,event_data):
        '''
        Funcao interna da classe Splunk para envio de dados via thread
        Nao pode ser chamada pelo objeto instanciado
        INPUT: string/dict event_data
        '''
        try:
            session = requests.Session()
            spk_result = session.post(self.export_url, data=event_data, headers=self.headers, verify=False, timeout=self.timeout)
        except Exception as e:
            raise Exception('Falha ao exportar dados pra Splunk >> '+str(e)+' <<')
        else:
            if(spk_result.status_code != 200):
                raise Exception('Retorno Splunk STATUS_CODE='+str(spk_result.status_code)+' >> '+str(spk_result.text)+' <<')
        finally:
            session.close()

    def send_to_splunk(self,host,source,event):
        '''
        Funcao para envio de dados em formato json para o Splunk Itau
        INPUT: string event_host
               string event_source
               string/dict event_data
        '''
        event_data = '{"host":"'+host+'","source":"'+source+'","event":'+json.dumps(event)+'}' 

        Process(target=self._export,args=(event_data,)).start()
