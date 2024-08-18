![Bangsue_Image](bangsue.jpg)

# Bangsue
Thai Codename Generator (Data from data.go.th / Wikipedia)

## Installation

    pip install bangsue
 ---
 ##  Example Code
 
    from bangsue_codename import *
    p = BangsueCodename.ThailandDistrict()
    codename = p.get_code_name()
    print(p.convert_codename_to_string(codename, "all"))
    
    RESULT : khaoyai_aoluek_krabi