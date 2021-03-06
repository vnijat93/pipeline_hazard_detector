import logging

from constants import (
    THREE_OPERANDS,
    TIMING_SEQUENCE
)
from typing import List

logging.basicConfig(level=logging.DEBUG)


def process_instructions(instructions: str, forwarding=False):

    global REGISTERS
    REGISTERS = {}
    instructions = sanitize_instructions(instructions.split("\r\n"))
    results = []

    i = 0
    pre_seq = []
    for instruction in instructions:

        logging.info(f"Process instruction {instruction}")
        result = {}
        result["instruction"] = instruction

        cur_seq = generate_sequence(instruction, pre_seq, forwarding)

        logging.info(f"current: {cur_seq}. previous: {pre_seq}")
        pre_seq = cur_seq

        result["sequence"] = cur_seq

        results.append(result)

        i += 1

        if i == len(instructions):
            column_count = len(cur_seq)

    return results, column_count


def generate_sequence(cur_ins, pre_seq, forwarding):

    sequence = []
    opcode = cur_ins.split(' ')[0]
    dest_reg = cur_ins.split(' ')[1]
    src_reg_1 = cur_ins.split(' ')[2]
    src_reg_2 = ''

    if not forwarding:
        cycles = 3
    else:
        if opcode == 'lw':
            cycles = 2
        else:
            cycles = 0

    if opcode in THREE_OPERANDS:
        src_reg_2 = cur_ins.split(' ')[3]

    if len(pre_seq) == 0:
        add_register(dest_reg, cycles)
        update_registers()
        return TIMING_SEQUENCE

    else:
        sequence = [''] * (pre_seq.index('ID')) + ["IF"]

        if opcode == 'sw':
            stall_cycles = get_stall_cycles(src_reg_1, src_reg_2, dest_reg)
        else:
            stall_cycles = get_stall_cycles(src_reg_1, src_reg_2, dest_reg)
        sequence += ['S'] * stall_cycles
        sequence += ["ID", "EX", "ME", "WB"]

        for _ in range(0, stall_cycles):
            update_registers()
            logging.info(f"regiters after updating {REGISTERS}")

    add_register(dest_reg, cycles)
    update_registers()
    return sequence


def get_stall_cycles(src_reg_1: str, src_reg_2: str, dest_reg=None):

    cycle_0 = REGISTERS.get(dest_reg, 0)

    if src_reg_1.startswith('$') or src_reg_1.endswith(')'):

        if src_reg_1.endswith(')'):
            start = src_reg_1.find('(')
            end = src_reg_1.find(')')

            src_reg_1 = src_reg_1[start+1:end]

        # This is a register
        cycle_1: int = REGISTERS.get(src_reg_1, 0)
        print(src_reg_1, cycle_1)

    if src_reg_2.startswith('$'):
        # This is a register
        cycle_2: int = REGISTERS.get(src_reg_2, 0)
        print(src_reg_2, cycle_2)
    elif src_reg_2 == '':
        cycle_2 = 0

    return max(cycle_0, cycle_1, cycle_2)


def add_register(reg, cycles):

    logging.info(f"adding {reg} to the registers {REGISTERS}")
    REGISTERS[reg] = cycles
    return


def update_registers():

    print(REGISTERS)

    for k, v in REGISTERS.items():

        if v != 0:
            REGISTERS[k] = v - 1

    return


def sanitize_instructions(instructions: List) -> List:

    results = []
    for instruction in instructions:

        if instruction != "":
            instruction = instruction.replace("\r", '')
            instruction = instruction.replace(",", '')
            results.append(instruction)
    return results


# instructions = """
# add $r1, $r2, $r3
# sub $r4, $r1, $r5
# and $r6, $r1, $r7
# or $r8, $r1, $r9
# """
# process_instructions(instructions)
