from easy_splunk import Splunk

try:
    spk = Splunk(protocol="https", url="10.0.0.2", port="8088", hec_key="e51e9c62-5f25-46cf-9a4e-218638cdab77")
except:
    raise