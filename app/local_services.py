from k2.service.local import service_installers

def services():
    return [inst.service() for _, inst in service_installers.items()]


def installer(service_name):
    return service_installers[service_name]
                