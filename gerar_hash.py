from pwdlib import PasswordHash


senha_context = PasswordHash.recommended()


hash_senha = senha_context.hash("123456")


print(hash_senha)