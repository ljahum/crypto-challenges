import Crypto.PublicKey.ECC as ecc

ecckey = ecc.import_key(open("secp256k1.pem", "r").read())
print(ecckey)

key  = ecc.generate(curve='P-384')
print(key)


pemk = key.export_key(format='PEM')
print(pemk)
