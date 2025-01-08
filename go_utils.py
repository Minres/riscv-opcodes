import logging
import pprint
import subprocess
import sys

from shared_utils import InstrDict, signed

pp = pprint.PrettyPrinter(indent=2)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:: %(message)s")


def make_go(instr_dict: InstrDict):

    args = " ".join(sys.argv)
    prelude = f"""// Code generated by {args}; DO NOT EDIT."""

    prelude += """
package riscv

import "cmd/internal/obj"

type inst struct {
	opcode uint32
	funct3 uint32
	rs1    uint32
	rs2    uint32
	csr    int64
	funct7 uint32
}

func encode(a obj.As) *inst {
	switch a {
"""

    endoffile = """  }
	return nil
}
"""

    instr_str = ""
    for i in instr_dict:
        enc_match = int(instr_dict[i]["match"], 0)
        opcode = (enc_match >> 0) & ((1 << 7) - 1)
        funct3 = (enc_match >> 12) & ((1 << 3) - 1)
        rs1 = (enc_match >> 15) & ((1 << 5) - 1)
        rs2 = (enc_match >> 20) & ((1 << 5) - 1)
        csr = (enc_match >> 20) & ((1 << 12) - 1)
        funct7 = (enc_match >> 25) & ((1 << 7) - 1)
        instr_str += f"""  case A{i.upper().replace("_","")}:
    return &inst{{ {hex(opcode)}, {hex(funct3)}, {hex(rs1)}, {hex(rs2)}, {signed(csr,12)}, {hex(funct7)} }}
"""

    with open("inst.go", "w", encoding="utf-8") as file:
        file.write(prelude)
        file.write(instr_str)
        file.write(endoffile)

    try:
        subprocess.run(["go", "fmt", "inst.go"], check=True)
    except:  # pylint: disable=bare-except
        pass
