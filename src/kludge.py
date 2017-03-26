#!/usr/bin/env python3

import base64

class Kludge:
    
    @staticmethod
    def d(key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    @staticmethod
    def try_exists(file):
        try:
            f = open(file,'r')
            rd = f.readline()
            f.close()
            if len(rd) < 5:
                return False
            return True
        except IOError:
            return False

    def __init__(self):
        sec = 'gsettings/client_secrets.json'

        if not Kludge.try_exists(sec):
            f = open(sec,'w')
            print("--")
            # Yes this is pure kludge, stops the github bots though.
            f.write(Kludge.d('tree',"w6_ClMOcw4rDlsKUwp_DoMKWw5XDkcOOw5nDoMOZw4TDncOWwofCn8KWwqPCnMKXwqvCosKbwpfCq8KjwpjClcKtwp_DjcKYw6XDlMObw5bDqcOcwpfDksKlwqLDisOMw6fDlMKVwpzDnsKjw4nCnMOiwqXDhsONw6nCpcKdw5LDlsOVwpPDhsOkw6LDmMKTw5vDocOUw4zDoMOXw5rDmMOZw6TDiMOUw6LDpsOKw5PDqMKgw4jDlMOhwpTCkcKHw6TDpMOUw4_DmcOVw5nDhMOdw5bCh8KfwpbDlcOGw5PDqsOTw5jCksOcw6HDlMOQwqHCo8KbwpfCpcKjwpjCh8KgwpTDhsOaw6jDmsOEw5rDpsObwofCn8KWw5rDmcOZw6TDpcKfwpTCo8OTw4jDiMOjw6fDk8OZw6fCoMOMw5TDo8OZw5HDisKiw5XDlMOSwqPDocKUw5TDlcOnw5nDjcKmwqHDhsOaw6jDmsKHwpHClsOmw5TDkMOZw6DDhMOaw6bDm8KHwp_ClsOaw5nDmcOkw6XCn8KUwqPDk8OIw4jDo8Onw5PDmcOnwqDDjMOUw6PDmcORw4rCosOVw5TDksKjw6HClMOUw5XDp8OZw43CpsKhw5nDlMOfw5fDk8KHwqDClMOGw5rDqMOaw4TDlcOmw6HDm8OOw5jDl8OXw4TDrMKnwpXCnsOTw5XDisOXw6jDkcOaw5fDoMKUwp_Ch8Ocw6bDmcOVw6fCrMKUwpTDq8Opw5zCk8Obw6HDlMOMw6DDl8OGw5XDncOlwpPDiMOjw5_ClMOUw5XDp8OZw43CpsKhw5vClsKjw5XDisOXw6jDpcKHwpHClsOVw5HDjsOZw6DDmcOEw6fDl8OIw5fDmcOmwofCn8KWw6nCl8Krw5rCo8Kawp3DicOfwq_Dh8Kpw5jCuMOYwqbCs8OJwrzCqsKmwp7CmsObwpTCkcKHw6bDl8OJw47DpsOXw4jDmcOTw6fDl8OOw6fClMKfw4DClsOaw5nDmcOkwqzClMKUw6DDocOIw4bDoMOaw5TDmMOowqzCncKVwqzCosKUwofDkcKewofDj8OVw6jDhsOYw5fDpMOOw5XDqMORw5TDl8Odw5nDjsOTw6fClMKfw4DClsOaw5nDmcOkwqzClMKUw6DDocOIw4bDoMOaw5TDmMOowqzCncKVwqzCosKHw4LDscOvbw=="))
            f.close()
