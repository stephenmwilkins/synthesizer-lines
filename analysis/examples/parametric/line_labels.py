

labels = {
    'O 2 3726.03A,O 2 3728.81A': '[OII]3726,3729',
    'H 1 4862.69A': r'H\beta',
    'O 3 4958.91A,O 3 5006.84A': '[OIII]4959,5007',
    'H 1 6564.62A': r'H\alpha',
    'O 3 5006.84A': '[OIII]5007',
    'N 2 6583.45A': '[NII]6583',
    'N 2 6583.45A': '[NII]6583',
    'Ne 3 3868.76A': 'Ne 3 3868.76A',
    'O 1 6300.30A': 'O 1 6300.30A',
    "S 2 6730.82A": "S 2 6730.82A",
    "S 2 6716.44A": "S 2 6716.44A",


}


def diagram_label(diagram):

    # x-axis
    numerator = labels[','.join(diagram[0][0])]
    denominator = labels[','.join(diagram[0][1])]
    x = f'{numerator}/{denominator}'
    # y-axis
    numerator = labels[','.join(diagram[1][0])]
    denominator = labels[','.join(diagram[1][1])]
    y = f'{numerator}/{denominator}'

    return x,y