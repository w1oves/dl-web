ip_address = "202.38.71.247"
import socket
import sh
def _net_is_used(port: int) -> bool:
    """
    判断端口port是否在使用中
    """
    try:
        str(sh.lsof(f"-i:{port}"))
        return True
    except:
        return False
for port in range(9000,9100):    
    print(port,_net_is_used(port))
