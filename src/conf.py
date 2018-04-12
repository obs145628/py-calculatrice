from .code_parser import  ParserOptions

conf = ParserOptions(

    enable_int=True,
    enable_real=True,
    enable_sqstring=True, #'...'
    enable_dqstring=True, #"..."
    enable_com1=True, # //...
    enable_com2=True, #/* */

    keywords=[
        'class',
        'end',
        'in',
        'let'
    ],

    ops=  [
        '(',
        ')',
        ',',
        '+',
        '-',
        '*',
        '/',
        '=',
        '&, '
        '|',
        '==',
        '!=',
        '^',
        '&&',
        '||',
        '!'
    ]
)