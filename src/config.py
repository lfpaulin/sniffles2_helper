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
            mosaic      Parse information of Sniffles2 mosaic calls
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
    subparser_genotypesv = subparsers.add_parser("sv", help=genotype_sv_help)
    subparser_genotypesv.add_argument('-m', '--min-support', type=int, required=False, dest='minsupp', default=1,
                                      help='Min. read support for the SV calls, default = 1')
    subparser_genotypesv.add_argument('-s', '--min-size', type=int, required=False, dest='minsize', default=1,
                                      help='Min. SV size, default = 1, in case of BND this is skipped')
    subparser_genotypesv.add_argument('-g', '--genotype-filter', type=str, required=False, dest='filer_gt', default="",
                                      help='Removed genotypes from output, for multiple,need to be comma separated.' +
                                      '\nExample: -f 0/0,0/1, default = None')
    subparser_genotypesv.add_argument('-f', '--filter', type=str, required=False, dest='filer_by', default="",
                                      help='')
    subparser_genotypesv.add_argument('-b', '--bed', action='store_true', required=False, dest='as_bed', default=False,
                                      help='')
    subparser_genotypesv.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False,
                                      help='')

    # Sniffles2 population
    snf2pop_help = "Perform analysis on Sniffles2 population-merges"
    subparser_snf2pop = subparsers.add_parser("population", help=snf2pop_help)
    subparser_snf2pop.add_argument('-m', '--min-support', type=int, required=False, dest='minsupp', default=1,
                                   help='Min. support for the SV calls (from SUPP_VEC), default = 1')
    subparser_snf2pop.add_argument('-s', '--min-size', type=int, required=False, dest='minsize', default=1,
                                   help='Min. absolute size of the event (except for BDN), default = 1')
    subparser_snf2pop.add_argument('-u', '--uniq-only', action='store_true', required=False, dest='uniq_only',
                                   help='Show only those that appear in a single individual (from SUPP_VEC), ' +
                                   'default = False')
    subparser_snf2pop.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False, help='')

    # Cancer
    sniffles2_cancer_help = "Cancer pipeline"
    sniffles2_cancer = subparsers.add_parser("cancer", help=sniffles2_cancer_help)
    sniffles2_cancer.add_argument('-u', '--uniq',  action='store_true', required=False, dest='uniq', default=False,
                                  help='Show unique calls only')
    sniffles2_cancer.add_argument('-m', '--mosaic',  action='store_true', required=False, dest='tumor_mosaic', 
                                  default=False, help='Show unique calls only')
    sniffles2_cancer.add_argument('-g', '--germline',  action='store_true', required=False, dest='tumor_germline', 
                                  default=True, help='Show unique calls only')
    sniffles2_cancer.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False, help='')

    # Mosaic
    sniffles2_mosaic_help = "Mosaic calls"
    sniffles2_mosaic = subparsers.add_parser("mosaic", help=sniffles2_cancer_help)
    sniffles2_mosaic.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False, help='')

    # Survivor
    survivor_help = "Perform analysis on SURVIVOR merges"
    subparser_survivor = subparsers.add_parser("survivor", help=survivor_help)
    subparser_survivor.add_argument('-1', '--1bp', action='store_true', required=False, dest='bp1',
                                    help='Get calls that start in the same coordinates and are different')
    subparser_survivor.add_argument('-t', '--support-threshold', type=int, required=False, dest='supp_threshold',
                                    default=1, help='Minimum number of callers in SUPP_VEC (default: 1)')
    subparser_survivor.add_argument('-u', '--filter-uniq', type=str, required=False, dest='filter_uniq',
                                    default="", help='Output only the SV that are in the given sample,'
                                                     'If no match will stop and return nothing, if empty will')
    subparser_survivor.add_argument('-p', '--filter-present', type=str, required=False, dest='with_overlap',
                                    default="", help='Output the SV that are present in a given sample,'
                                                     'If no match will stop and return nothing')
    subparser_survivor.add_argument('-!', '--dev', action='store_true', required=False, dest='as_dev', default=False, help='')

    # ############################################################################################ #

    args = parser.parse_args()
    return args, snf2_help

