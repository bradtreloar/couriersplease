
import re

from couriersplease.enum import street_addr_suffix



def condense_address(addr, field_lengths):
    # convert address to uppercase to simplify pattern-matching
    addr = addr.upper()

    # abbreviate street suffix if address is longer than maxlength
    if not address_fits_in_fields(addr, field_lengths):
        for suffix, abbr in street_addr_suffix:
            addr = addr.replace(suffix, abbr)

    substitutions = [
        # abbreviate "U[NIT][ ]x, y" to "Ux/y"
        (r"U(NIT){0,1}\s+(\d+)[,/]{0,1}\s*(\d+)", r"U\2/\3"),

        # abbreviate "L[EVEL|VL] x" to "LVLx"
        (r"L(EVEL|VL)+\s+(\d+),{0,1}", r"LVL\2"),

        # abbreviate "BUILDING" to "BLDG"
        (r"BUILDING", r"BLDG"),

        # remove supplemental details in parentheses
        (r"[\(\[][\w\s]+[\)\]]", r""),

        # remove building name but leave level number
        (r"(LVL{0,1}\d+),{0,1} [\w\s]+,{0,1} (\d+)", r"\1 \2"),

        # remove vowels in middle of words
        (r"([^ ])[AEIOU]+", r"\1"),
    ]

    # apply regexp substitutions until addr is reduced to maxlength
    for rule in substitutions:
        # stop applying substitutions if we're under maxlength
        if address_fits_in_fields(addr, field_lengths):
            return addr

        # apply the substitution
        addr = re.sub(rule[0], rule[1], addr)

    # return the condensed address
    return addr



def address_fits_in_fields(addr, field_lengths):
    # split the address into components
    comps = addr.split()

    comp_index = 0
    for field_len in field_lengths:
        # start with no field contents
        content_len = 0

        # add components to the content length until the field is full or
        # we run out of components
        while content_len <= field_len:
            # add 1 for a space if this is not the start of the contents
            if content_len > 0:
                content_len += 1

            try:
                # add a component
                content_len += len(comps[comp_index])
                # move to the next component if we haven't overflowed the field
                if content_len <= field_len:
                    comp_index += 1
            except IndexError:
                # we used up all the components,
                # therefore the address fits in the fields
                return True

    # if we've still got components left over 
    # then the address doesn't fit in the fields
    return not comp_index < len(comps)