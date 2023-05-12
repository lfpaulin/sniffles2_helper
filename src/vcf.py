import logging as logger


AS_DEV = True
logger.basicConfig(level=logger.DEBUG) if AS_DEV else logger.basicConfig(level=logger.INFO)


# vcf header class
class VCFHeader(object):
    # init
    def __init__(self, input_line=None):
        self.SAMPLES = ""
        if input_line is not None:
            # save the original
            self.vcf_header = input_line
            # vcf files have 9 fields + the samples/genomes data
            # split and analysis
            VCF_MANDATORY_FIELDS = 9
            tab_sep_fields = input_line.split("\t")
            self.ERROR = len(tab_sep_fields) < VCF_MANDATORY_FIELDS   # 9 VCF fields + genotypes
            if not self.ERROR:
                # extract mandatory fields
                self.SAMPLES = tab_sep_fields[VCF_MANDATORY_FIELDS:]
        else:
            self.ERROR = True


# vcf line class for single individuals SV
class VCFLineSV(object):
    # init
    def __init__(self, input_line):
        # save the original
        self.sv_line = input_line
        # vcf files have 9 fields + the samples/genomes data
        # split and analysis
        VCF_MANDATORY_FIELDS = 9
        tab_sep_fields = input_line.split("\t")
        self.ERROR = len(tab_sep_fields) < VCF_MANDATORY_FIELDS   # 9 VCF fields + genotypes
        if not self.ERROR:
            # extract mandatory fields
            # not used REF, as _
            [self.CHROM, POS, self.ID, _, ALT, self.QUAL, self.FILTER, INFO,
             FORMAT] = tab_sep_fields[:VCF_MANDATORY_FIELDS]
            self.POS = int(POS)
            # for INFO -> get_parsed_info()
            self.BREAKPOIN = ""
            self.SVTYPE = ""
            self.SVLEN = 0
            self.END = -1
            self.SUPPORT = 0
            self.COVERAGE = []
            self.STRAND = ""
            self.STDEV_LEN = -1
            self.STDEV_POS = -1
            self.RNAMES = []
            self.SUPPORT_LONG = 0
            self.AF = "NA"
            # for FORMAT -> get_genotype()
            self.GENOTYPE = ""
            self.GQ = ""
            self.DR = 0
            self.DV = 0
            # parse data
            self.get_genotype(tab_sep_fields[VCF_MANDATORY_FIELDS], FORMAT)
            self.get_parsed_info(INFO)
            # for Translocation (BND/TRA)
            self.AF = self.DV/(self.DV+self.DR) if (self.AF == "NA" and self.DV+self.DR != 0) else self.AF
            self.TRA = "" if self.SVTYPE != "BND" else ALT
            self.END = self.END if self.SVTYPE != "BND" else self.POS + 1
            self.SVLEN = int(self.SVLEN) if self.SVTYPE != "BND" else self.SVLEN

    def get_parsed_info(self, info_string):
        # INFO field extraction
        extract_info = ["SVTYPE", "SVLEN", "END", "SUPPORT", "COVERAGE", "STRAND", "STDEV_LEN", 
                        "STDEV_POS", "RNAMES", "SUPPORT_LONG", "AF"]
        for each_info in info_string.split(";"):
            if "=" not in each_info:
                self.BREAKPOIN = each_info
            else:
                [info_key, info_val] = each_info.split("=")
                if info_key in extract_info:
                    self.SVTYPE = info_val if info_key == "SVTYPE" else self.SVTYPE
                    self.SVLEN = info_val if info_key == "SVLEN" else self.SVLEN
                    self.END = int(info_val) if info_key == "END" else self.END
                    self.SUPPORT = int(info_val) if info_key == "SUPPORT" else self.SUPPORT
                    self.COVERAGE = [int(x) for x in info_val.split(",")] if info_key == "COVERAGE" else self.COVERAGE
                    self.STRAND = info_val if info_key == "STRAND" else self.STRAND
                    self.AF = float(info_val) if info_key == "AF" else self.AF
                    self.STDEV_LEN = float(info_val) if info_key == "STDEV_LEN" else self.STDEV_LEN
                    self.STDEV_POS = float(info_val) if info_key == "STDEV_POS" else self.STDEV_POS
                    self.RNAMES = info_val.split(",") if info_key == "RNAMES" else self.RNAMES
                    self.SUPPORT_LONG = int(info_val) if info_key == "SUPPORT_LONG" else self.SUPPORT_LONG

    # extract information from the "FORMAT" field and each sample
    def get_genotype(self, _sample, _format):
        # FORMAT field and genotype extraction
        extract_genotype = ["GT", "GQ", "DR", "DV"]
        # single individual in the vcf file
        split_format = _format.split(":")
        split_gt = _sample.split(":")
        for gt_format, gt_value in zip(split_format, split_gt):
            if gt_format in extract_genotype:
                self.GENOTYPE = gt_value if gt_format == "GT" else self.GENOTYPE
                self.GQ = int(gt_value) if gt_format == "GQ" else self.GQ
                self.DR = int(gt_value) if gt_format == "DR" else self.DR
                self.DV = int(gt_value) if gt_format == "DV" else self.DV


# vcf line class for multi individual/population file
