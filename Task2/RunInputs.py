from EMail import check_mail
import json


def main():
    print('Deserializing inputs from inputs.json...')
    j_inputs = []
    with open('inputs.json', 'r') as f:
        j_inputs = json.load(f)
    
    inps = []
    for j_inp in j_inputs:
        h = j_inp.split(':')
        inp = ''.join(chr(int(c, 16)) for c in h)
        inps.append(inp)

    print('Deserialized.')

    print('Now running check_mail in these inputs')
    for inp in inps:
        check_mail(inp)


if __name__ == "__main__":
    main()
