import qs_module


def reponse_function(req):
    print("Item: ", req)
    return "Thanks for connection..."


qs_module.__init__("127.0.0.1",2529,1000,reponse_function,http_response_=True,log_=True,counter=5)