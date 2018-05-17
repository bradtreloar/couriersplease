
import re

from couriersplease.enum import street_addr_suffix


class Address:


    @staticmethod
    def split_into_fields(addr, field_lengths):
        'Splits a string into fields'

        # Split the joined string into components.
        comps = addr.split()

        # Initialise an index pointer so we can
        # iterate over the components in a while loop
        ci = 0

        # Initialise an empty list for the 
        # output address.
        output = ["" for i in range(len(field_lengths))]

        for i, field_len in enumerate(field_lengths):
            # Add components to the field until it is full or
            # we run out of components.
            while len(output[i]) <= field_len:
                # Get the next component.
                comp = comps[ci]

                # Check whether the next component will fit into
                # the remaining space in this field
                if (len(output[i]) + 1 + len(comp)) > field_len:
                    # move to the next field
                    break
                
                # Add a space if this is not the start of the contents.
                if output[i] != "":
                    output[i] += " "

                # add the component to the field
                output[i] += comp

                # move to the next field
                ci += 1
                # We can return the address if we've
                # got no more components to add
                if ci >= len(comps):
                    return output

        # If we've still got components left over 
        # then the address doesn't fit in the fields,
        # so we return nothing rather than a partial address.
        [print(x) for x in output]
        return None


    @staticmethod
    def condense(address, field_lengths):
        # Join the address into a single uppercase string
        output = " ".join(address).upper()

        # Abbreviate street suffix if address is longer than maxlength.
        if not Address.fits_into_fields(output, field_lengths):
            for suffix, abbr in street_addr_suffix:
                output = output.replace(suffix, abbr)

        substitutions = [
            # Abbreviate "U[NIT][ ]x, y" to "Ux/y".
            (r"U(NIT){0,1}\s+(\d+)[,/]{0,1}\s*(\d+)", r"U\2/\3"),

            # Abbreviate "L[EVEL|VL] x" to "LVLx".
            (r"L(EVEL|VL)+\s+(\d+),{0,1}", r"LVL\2"),

            # Abbreviate "BUILDING" to "BLDG".
            (r"BUILDING", r"BLDG"),

            # Remove supplemental details in parentheses.
            (r"[\(\[][\w\s]+[\)\]]", r""),

            # Remove building name but leave level number.
            (r"(LVL{0,1}\d+),{0,1} [\w\s]+,{0,1} (\d+)", r"\1 \2"),

            # Remove vowels in middle of words.
            (r"([^ ])[AEIOU]+", r"\1"),
        ]

        # Apply regexp substitutions until addr is reduced to maxlength
        for rule in substitutions:
            # stop applying substitutions if we're under maxlength
            if Address.fits_into_fields(output, field_lengths):
                break

            # apply the substitution
            output = re.sub(rule[0], rule[1], output).strip()

        # Return the condensed address, split into fields
        return Address.split_into_fields(output, field_lengths)


    @staticmethod
    def fits_into_fields(addr, field_lengths):
        'Tests whether address will fit in fields.'

        # Split the address into components
        comps = addr.split()

        comp_index = 0
        for field_len in field_lengths:
            # Start with no field contents
            content_len = 0

            # Add components to the content length until the field is full or
            # we run out of components.
            while content_len <= field_len:
                # Add 1 for a space if this is not the start of the contents.
                if content_len > 0:
                    content_len += 1

                try:
                    # Add a component.
                    content_len += len(comps[comp_index])
                    # Move to the next component if we haven't overflowed the field.
                    if content_len <= field_len:
                        comp_index += 1
                except IndexError:
                    # We used up all the components,
                    # therefore the address fits in the fields.
                    return True

        # If we've still got components left over 
        # then the address doesn't fit in the fields.
        return not comp_index < len(comps)
