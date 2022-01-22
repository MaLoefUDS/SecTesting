def check_mail(addr: str):
    print('Input to check_mail: ', addr)

    if addr.find('.') == 10:
        if addr.find('@') == 3:
                prefix = addr[:3]
                if prefix.isupper():
                    if addr.endswith('.com'):
                        if 'wow' in addr:
                            print('Accepted! (com)')
                            return True
                        else:
                            print('Not accepted! wow not found. (com)')
                            return False
                    elif addr.endswith('.de'):
                        if 'such' in addr:
                            print('Accepted! (de)')
                            return True
                        else:
                            print('Not accepted! such not found. (de)')
                            return False
                    elif addr.endswith('.fr'):
                        if 'fuzz' in addr:
                            print('Accepted! (fr)')
                            return True
                        else:
                            print('Not accepted! fuzz not found. (fr)')
                            return False
                    else:
                        print('Not accepted! (invalid)')
                        return False
                else:
                    print('Not accepted! (prefix not upper)')
                    return False
        else:
            print('Not accepted! (@ not in expected range)')
            return False
    else:
        print('Not accepted (. not at expected position)')
        return False