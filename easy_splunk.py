from requests import Session
from multiprocessing import Process
import json
import socket

class Splunk():
    '''
    Splunk() class is responsible for the abstraction of the connection and main functions available in Splunk API.
    Its attributes represent the configuration parameters of the Splunk connection, such as: 
        - URL / IP;
        - Connection port (514 syslog / 8088 HEC);
        - HTTP Event Collector (HEC) key;
        - Connection timeout;
    Its methods abstract the Splunk API complexity, making these APIs available by just setting the minimum arguments required.
        - print(): print all splunk object attributes as json;
        - send_data(): send data to Splunk by HEC/syslog;

    INPUT:
        - string protocol (options: "http" / "https" / "syslog")
        - string url (examples: "splunk.domain" / "10.0.0.100")
        - int port (examples: "8088" / "514")
      * - string hec_key (example: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
      * - int timeout (default: "30")

        * optative
    '''
    def __init__(self, protocol, url, port, hec_key=None, timeout=30):
        self.protocol = protocol
        self.url = url
        self.port = port
        self.hec_key = hec_key
        self.timeout = timeout
        self._headers = { 'Authorization': 'Splunk ' + self.hec_key }
        self._export_url = f'{ self.protocol }://{ self.url }:{ self.port }/services/collector/event'
        # self.headers = { 'Authorization': 'Splunk ' + self.key }
        # self.export_url = f'{ self.url }/services/collector/event'

        self._session = Session()
        # self.session = Session()

        
    def __str__(self):
        '''
        Return a string (json format) with all the attributes for the Splunk object.
        Used when print(obj) is called.

        OUTPUT: 
            - string protocol
            - string url
            - int port
            - int timeout
          * - string hec-key

            * if defined
        '''
        attributes = {}
        attributes['url'] = self.url
        attributes['protocol'] = self.protocol
        attributes['port'] = self.port
        attributes['timeout'] = self.timeout
        if self.hec_key:
            attributes['hec_key'] = self.hec_key
        return str(attributes)


    def _export(self, event_data):
        '''
        Private method responsible for sending data to Splunk.
        Called by "multiprocessing" class, allowing parallel data exportation.
        
        INPUT:
            - dict event_data
        '''
        try:
            print(self._export_url)
            print(self._headers)
            spk_out = self._session.post(url=self._export_url, data=event_data, headers=self._headers, verify=False, timeout=self.timeout)
        except Exception as e:
            raise Exception(f'Unable to connect to Splunk { self.url }: { str(e) }')
        else:
            if spk_out.status_code != 200:
                raise Exception(f'Unexpected status code { str(spk_out.status_code) } received from Splunk { self.url }: { str(spk_out.text) }')


    def send_data(self, event_host, event_source, event_data):
        '''
        Method responsable for structure the data JSON as Splunk expects and call the _export() private method.

        INPUT: 
            - string event_host
            - string event_source
            - string/dict event_data
        '''
        # event_data = '{"host":"'+host+'","source":"'+source+'","event":'+json.dumps(event)+'}' 
        event_data = {}
        event_data['host'] = event_host
        event_data['source'] = event_source
        event_data['event'] = json.dumps(event_data)

        Process(target=self._export, args=(event_data,)).start()
        # Process(target=self._export, args=(str(event_data),)).start()
