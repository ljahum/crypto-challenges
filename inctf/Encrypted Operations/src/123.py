from rich.traceback import install
install()
# -----------------------------------

print(1/0)
# -----------------------------------
name=input("name:")
age=input("age:")

msg=f'''
---------------information of {name}---------------
Name:{name}
Age :{age}
-----------------end------------------------
'''


