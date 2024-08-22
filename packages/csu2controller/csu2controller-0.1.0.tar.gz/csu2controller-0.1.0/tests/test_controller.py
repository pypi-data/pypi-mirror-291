from csu2controller.csu2controller import CSU2Controller

my_controller = CSU2Controller()
my_controller.connect()

resp = my_controller.query_ok()

print(resp)