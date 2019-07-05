from easy_splunk import Splunk


host = "EVENT_HOST"
source = "EVENT_SOURCE"


try:
    spk_hec = Splunk(protocol="https", url="10.0.0.2", port="8088", 
        hec_key="e51e9c62-5f25-46cf-9a4e-218638cdab77")
    spk_syslog = Splunk(protocol="syslog", url="10.0.0.2", port="5514", timeout=60)
except:
    raise


#Send a dict data as JSON to Splunk API
data_hec = {}
data_hec["Key_1"] = "Valor_1"
data_hec["Key_2"] = "Valor_2"
data_hec["Key_3"] = "Valor_3"
spk_hec.send_data(event_host=host, event_source=source, event_data=data_hec)
spk_hec.send_data(event_source=source, event_data=data_hec)

#Send a basic syslog message to Splunk
data_syslog = "Syslog message sent by easy_splunk"
spk_syslog.send_data(event_data=data_syslog)

#Run a specific search and get the result as a list of JSONs
search = 'index=raw_syslog | head 3'
search_output = spk_hec.run_search(username='admin', password='dsh1991dsh', search=search)
print(search_output)