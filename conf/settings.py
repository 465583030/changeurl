# -*- coding:utf-8 -*-

CODING = 'utf8'

# socket
ip_port = ('127.0.0.1',9527)
link_num = 88

# mysql conf
host = "localhost"
user = 'root'
password = '123456'
database = 'changeurl'
db_port = '3306'

s = 'key=000000fghjfghj00000&cookie=pgv_pvid%3D283938062%3B+pt2gguin%3Do0757588331%3B+ptcz%3Dd38c4ced6d26ed9e0fcd52de2bf5bd92fd167a4f573c1356c8898c2a85f4cb42%3B+o_cookie%3D835805290%3B+pac_uid%3D1_757588331%3B+RK%3DGdtDNRQae0%3B+pgv_pvi%3D2446087168%3B+&ptui_loginuin%3D835805290%3B+pgv_si%3Ds4197686272%3B+ptisp%3Dcnc%3B+uin%3Do0757588331%3B+skey%3DMVXmmhEAKh%3B+p_uin%3Do0757588331%3B+p_skey%3D8c7feVIwihxuX-2QwLllINJZdtGE9qfPJLy9WFWreEI_%3B+pt4_token%3DnKlsCwRfnDvf4pZoTLMz8C7jtEsX5KbNpiSo2qAN6FA_'

if __name__ == '__main__':
    import re
    print(s.split('&'),len(s.split('&')))
    print(re.split('[&]',s,1),len(re.split('[&]',s,1)))
    print(re.split('[&]',s,2),len(re.split('[&]',s,2)))
    # print(re.findall('[&]',s),len(re.findall('[&]',s)))
    # print(dict(s))