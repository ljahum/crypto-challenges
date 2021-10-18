from aes_dfa.attack import attack
normal_cipher_text = "81d6cdc3bd16fb8d72b9bb88818b5be9"
faulty_cipher_text = "eff93508630187b8d3494e8b70e6887e"
keys = attack(normal_cipher_text, faulty_cipher_text)
print(keys[0])