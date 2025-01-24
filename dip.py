def set_dip_switches(dmx_address):

    dip_switches = []

    for i in range(10):

        if dmx_address & (1 << i):
            dip_switches.append(True)
        else:
            dip_switches.append(False)


    answer = ''
    for i in range(len(dip_switches)):
        if dip_switches[i]:
            answer = answer + ' ' + str(i + 1)

    result = f'Адрес: {dmx_address}\nON: {answer}'

    return result