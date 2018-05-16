
import re

from couriersplease.enum import street_addr_suffix



def condense_address(addr, maxlength):
    # convert address to uppercase to simplify pattern-matching
    addr = addr.upper()

    # abbreviate street suffix if address is longer than maxlength
    if len(addr) > maxlength:
        for suffix, abbr in street_addr_suffix:
            addr = addr.replace(suffix, abbr)

    rules = [
        # abbreviate "U[NIT] x, y" to "Ux/y"
        (r"U(NIT ){0,1}(\d+)[,/]{0,1}\s*(\d+)", r"U\2/\3"),

        # abbreviate "L[EVEL|VL] x" to "Lx"
        (r"L(EVEL|VL)+\s{0,1}(\d+),{0,1}", r"LVL\2"),

        # abbreviate "BUILDING" to "BLDG"
        (r"BUILDING", r"BLDG"),

        # remove building name but leave level number
        (r"(LVL{0,1}\d+),{0,1} [\w\s]+,{0,1} (\d+)", r"\1 \2")
    ]

    # apply rules until addr is reduced to maxlength
    for rule in rules:
        # stop applying rules if we're under maxlength
        if len(addr) <= maxlength:
            break

        # apply the rule
        addr = re.sub(rule[0], rule[1], addr)

    # return the condensed address
    return addr