#!/usr/bin/env python3

import argparse
import json
import logging
import pprint

from c_utils import make_c
from chisel_utils import make_chisel
from constants import emitted_pseudo_ops
from go_utils import make_go
from latex_utils import make_latex_table, make_priv_latex_table
from rust_utils import make_rust
from shared_utils import add_segmented_vls_insn, create_inst_dict
from sverilog_utils import make_sverilog

LOG_FORMAT = "%(levelname)s:: %(message)s"
LOG_LEVEL = logging.INFO

pretty_printer = pprint.PrettyPrinter(indent=2)
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)


def generate_extensions(
    extensions: list[str],
    include_pseudo: bool,
    c: bool,
    chisel: bool,
    spinalhdl: bool,
    sverilog: bool,
    rust: bool,
    go: bool,
    latex: bool,
):
    instr_dict = create_inst_dict(extensions, include_pseudo)
    instr_dict = dict(sorted(instr_dict.items()))

    with open("instr_dict.json", "w", encoding="utf-8") as outfile:
        json.dump(add_segmented_vls_insn(instr_dict), outfile, indent=2)

    if c:
        instr_dict_c = create_inst_dict(
            extensions, False, include_pseudo_ops=emitted_pseudo_ops
        )
        instr_dict_c = dict(sorted(instr_dict_c.items()))
        make_c(instr_dict_c)
        logging.info("encoding.out.h generated successfully")

    if chisel:
        make_chisel(instr_dict)
        logging.info("inst.chisel generated successfully")

    if spinalhdl:
        make_chisel(instr_dict, True)
        logging.info("inst.spinalhdl generated successfully")

    if sverilog:
        make_sverilog(instr_dict)
        logging.info("inst.sverilog generated successfully")

    if rust:
        make_rust(instr_dict)
        logging.info("inst.rs generated successfully")

    if go:
        make_go(instr_dict)
        logging.info("inst.go generated successfully")

    if latex:
        make_latex_table()
        logging.info("instr-table.tex generated successfully")
        make_priv_latex_table()
        logging.info("priv-instr-table.tex generated successfully")


def main():
    parser = argparse.ArgumentParser(description="Generate RISC-V constants headers")
    parser.add_argument(
        "-pseudo", action="store_true", help="Include pseudo-instructions"
    )
    parser.add_argument("-c", action="store_true", help="Generate output for C")
    parser.add_argument(
        "-chisel", action="store_true", help="Generate output for Chisel"
    )
    parser.add_argument(
        "-spinalhdl", action="store_true", help="Generate output for SpinalHDL"
    )
    parser.add_argument(
        "-sverilog", action="store_true", help="Generate output for SystemVerilog"
    )
    parser.add_argument("-rust", action="store_true", help="Generate output for Rust")
    parser.add_argument("-go", action="store_true", help="Generate output for Go")
    parser.add_argument("-latex", action="store_true", help="Generate output for Latex")
    parser.add_argument(
        "extensions",
        nargs="*",
        help="Extensions to use. This is a glob of the rv_.. files, e.g. 'rv*' will give all extensions.",
    )

    args = parser.parse_args()

    print(f"Extensions selected : {args.extensions}")

    generate_extensions(
        args.extensions,
        args.pseudo,
        args.c,
        args.chisel,
        args.spinalhdl,
        args.sverilog,
        args.rust,
        args.go,
        args.latex,
    )

    return variable_mapping.get(variable_name, "Entry not in variable_mapping")


def map_assembly(variable_name):
    variable_mapping = {
        "rd": "name(rd)",
        "rt": "rt",
        "rs1": "name(rs1)",
        "rs2": "name(rs2)",
        "rs3": "rs3",
        "aqrl": "aqrl",
        "aq": "aq[0:0]",
        "rl": "rl[0:0]",
        "imm20": "imm[31:12]",
        "jimm20": "imm[20:20] :: imm[10:1] :: imm[11:11] :: imm[19:12]",
        "imm12": "imm",
        "csr": "csr",
        "imm12hi": "",
        "bimm12hi": "",
        "imm12lo": "imm",
        "bimm12lo": "imm",
        "shamtq": "shamtq",
        "shamtw": "shamtw",
        "shamtw4": "shamtw4",
        "shamtd": "shamtd",
        "bs": "bs",
        "rnum": "rnum",
        "rc": "rc",
        "imm2": "imm[1:0]",
        "imm3": "imm[2:0]",
        "imm4": "imm[3:0]",
        "imm5": "imm[4:0]",
        "imm6": "imm[5:0]",
        "zimm": "zimm",
        "opcode": "opcode",
        "funct7": "funct7",
        "vd": "vd",
        "vs3": "vs3",
        "vs1": "vs1",
        "vs2": "vs2",
        "vm": "vm",
        "wd": "wd",
        "amoop": "amoop",
        "nf": "nf",
        "simm5": "simm",
        "zimm5": "zimm",
        "zimm10": "zimm",
        "zimm11": "zimm",
        "zimm6hi": "zimm6hi",
        "zimm6lo": "zimm6lo",
        "c_nzuimm10": "imm[5:4] :: imm[9:6] :: imm[2:2] :: imm[3:3]",
        "c_uimm7lo": "uimm[2:2] :: uimm[6:6]",
        "c_uimm7hi": "uimm[5:3]",
        "c_uimm8lo": "c_uimm8lo",
        "c_uimm8hi": "c_uimm8hi",
        "c_uimm9lo": "c_uimm9lo",
        "c_uimm9hi": "c_uimm9hi",
        "c_nzimm6lo": "imm[4:0]",
        "c_nzimm6hi": "imm[5:5]",
        "c_imm6lo": "imm[4:0]",
        "c_imm6hi": "imm[5:5]",
        "c_nzimm10hi": "nzimm[9:9]",
        "c_nzimm10lo": "nzimm[4:4] :: nzimm[6:6] :: nzimm[8:7] :: nzimm[5:5]",
        "c_nzimm18hi": "imm[17:17]",
        "c_nzimm18lo": "imm[16:12]",
        "c_imm12": "imm[11:11] :: imm[4:4] :: imm[9:8] :: imm[10:10] :: imm[6:6] :: imm[7:7] :: imm[3:1] :: imm[5:5]",
        "c_bimm9lo": "imm[7:6] :: imm[2:1] :: imm[5:5]",
        "c_bimm9hi": "imm[8:8] :: imm[4:3]",
        "c_nzuimm5": "c_nzuimm5",
        "c_nzuimm6lo": "c_nzuimm6lo",
        "c_nzuimm6hi": "c_nzuimm6hi",
        "c_uimm8splo": "uimm[4:2] :: uimm[7:6]",
        "c_uimm8sphi": "uimm[5:5]",
        "c_uimm8sp_s": "uimm[5:2] :: uimm[7:6]",
        "c_uimm10splo": "c_uimm10splo",
        "c_uimm10sphi": "c_uimm10sphi",
        "c_uimm9splo": "c_uimm9splo",
        "c_uimm9sphi": "c_uimm9sphi",
        "c_uimm10sp_s": "c_uimm10sp_s",
        "c_uimm9sp_s": "c_uimm9sp_s",
        "c_uimm2": "uimm[0:0] :: uimm[1:1]",
        "c_uimm1": "uimm[1:1]",
        "c_rlist": "rlist[3:0]",
        "c_spimm": "spimm[5:4]",
        "c_index": "c_index",
        "rs1_p": "rs1[2:0]",
        "rs2_p": "rs2[2:0]",
        "rd_p": "rd[2:0]",
        "rd_rs1_n0": "rs1[4:0]",
        "rd_rs1_p": "rd[2:0]",
        "rd_rs1": "rs1[4:0]",
        "rd_n2": "rd[4:0]",
        "rd_n0": "rd_n0",
        "rs1_n0": "rs1[4:0]",
        "c_rs2_n0": "rs2[4:0]",
        "c_rs1_n0": "rs1[4:0]",
        "c_rs2": "rs2[4:0]",
        "c_sreg1": "rs1[2:0]",
        "c_sreg2": "rs2[2:0]",
        "fm": "fm[3:0]",
        "pred": "pred[3:0]",
        "succ": "succ[3:0]",
        "rm": "rm[2:0]",
    }
    return variable_mapping.get(variable_name, "Entry not in assembly_mapping")


def make_coredsl2(instr_dict):

    for inst_name, instr_info in instr_dict.items():
        enc = instr_info["encoding"]
        coredsl_enc = ""

        literal_builder = ""
        for pos, token in enumerate(enc):
            # build up the literal
            if token == "1" or token == "0":
                literal_builder += token
            else:
                # flush the builder
                if literal_builder:
                    coredsl_enc += f"{len(literal_builder)}'b{literal_builder} :: "
                    literal_builder = ""
                # check for variables
                for variable in instr_info["variable_fields"]:
                    variable_encoding = arg_lut[variable]
                    if len(enc) - pos - 1 == variable_encoding[0]:
                        coredsl_enc += f"{map_variable(variable)} :: "
        # flush builder at the end of encoding
        coredsl_enc += f"{len(literal_builder)}'b{literal_builder}"

        assembly = ""
        for pos, variable in enumerate(instr_info["variable_fields"]):
            assembly_entry = map_assembly(variable)
            # incase there's a two part variable skip emitting the skeleton
            if not assembly_entry:
                continue
            assembly += "{"
            assembly += f"{assembly_entry}"
            assembly += "}"
            if pos != len(instr_info["variable_fields"]) - 1:
                assembly += ", "

        to_check = ["rd", "rs1", "rs2"]
        rfs_checks = [f"{reg} >=RFS" for reg in to_check if reg in coredsl_enc]

        if rfs_checks:
            behavior = f'if({ " || ".join(rfs_checks)}) raise(0, 2);\n'
            behavior += "              else "
        else:
            behavior = ""
        if "rd" in coredsl_enc:
            behavior += "if(rd != 0)"
        behavior += "{\n              }"
        print(f"{inst_name.upper().replace('_','__')} {{")
        print(f"    encoding: {coredsl_enc};")
        if assembly:
            print(f'    assembly: "{assembly}";')
        print(f"    behavior: {behavior}")
        print("}")


if __name__ == "__main__":
    main()
