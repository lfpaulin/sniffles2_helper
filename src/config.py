import argparse


# Version
def the_version():
    print(f'sniffles2_helper 0.5')


# Arguments
def get_arguments():
    snf2_help = """
    vcf_utils <command> [<args>]
        # Parse VCF files:
            sv          Extract genotype information for SV
                            none | --min-support | --filter | --min-size

        # Software specific population-SV VCF files
            survivor    Parse information of SURVIVOR merge result
                            none | --1bp | --support-threshold  | --filter-uniq | --filter-present
            population  Parse information of Sniffles2 population merge result
                            none | ...
            cancer      Parse information of Sniffles2 population merge result
                            none | ...

        # Version
            version    Shows current version/build
    """
    parser = argparse.ArgumentParser(
             description="Sniffles2 helper",
             usage=snf2_help
    )
    subparsers = parser.add_subparsers(help=snf2_help, dest="command")

    # ############################################################################################ #
    # Version
    version_help = "Gives the version number"
    subparser_version = subparsers.add_parser("version", help=version_help)
    subparser_help = subparsers.add_parser("help", help="")

    # ############################################################################################ #
    # Parse VCF files
    # Single sample sniffles2 SV file
    genotype_sv_help = "Extracts the chr, position and genotype for SV"
    subparser_genotypesv = subparsers.add_parser("svgt", help=genotype_sv_help)
    subparser_genotypesv.add_argument('-m', '--min-support', type=int, required=False, dest='minsupp', default=1,
                                      help='Min. read support for the SV calls, default = 1')
    subparser_genotypesv.add_argument('-s', '--min-size', type=int, required=False, dest='minsize', default=1,
                                      help='Min. SV size, default = 1, in case of BND this is skipped')
    subparser_genotypesv.add_argument('-f', '--filter', type=str, required=False, dest='filer_gt', default="",
                                      help='Removed genotypes from output, for multiple,need to be comma separated.' +
                                      '\nExample: -f 0/0,0/1, default = None')
    subparser_genotypesv.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False, help='')

    # Sniffles2 population
    snf2pop_help = "Perform analysis on Sniffles2 population-merges"
    subparser_snf2pop = subparsers.add_parser("snf2Pop", help=snf2pop_help)

    # Cancer
    sniffles2_cancer_help = "Cancer pipeline"
    sniffles2_cancer = subparsers.add_parser("snf2can", help=sniffles2_cancer_help)

    # Survivor
    survivor_help = "Perform analysis on SURVIVOR merges"
    subparser_survivor = subparsers.add_parser("survivor", help=survivor_help)

    # ############################################################################################ #

    args = parser.parse_args()
    return args, snf2_help

