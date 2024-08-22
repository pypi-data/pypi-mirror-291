from argparse import ArgumentParser, Namespace
from contextlib import contextmanager
from sys import exit
from . import __about__
from .core import Archive, dlarchive

parser = ArgumentParser(allow_abbrev=False)


def main():
    parser.add_argument('--version', '-v', action='version', version=f'wfarchive {__about__.__version__}')
    subparsers = parser.add_subparsers(required=True)

    parser_load = subparsers.add_parser('load', aliases=['l'])
    parser_load.set_defaults(func=load)
    subparsers_load = parser_load.add_subparsers(required=True)

    parser_load_fetch = subparsers_load.add_parser('fetch', aliases=['f'])
    parser_load_fetch.set_defaults(fetch=True)
    parser_load_fetch.add_argument('wflow_id')
    parser_load_fetch.add_argument('--exist-ok', '-f', action='store_true')
    parser_load_fetch.add_argument('--export-loose-files', '-l', metavar='target_directory', nargs='?', action='append')
    parser_load_fetch.add_argument('--export-archive', '-a', metavar='target_file', nargs='?', action='append')
    parser_load_fetch.add_argument('--export-signed-archive', '-s', metavar='target_file', nargs='?', action='append')

    parser_load_local = subparsers_load.add_parser('local', aliases=['l'])
    parser_load_local.set_defaults(fetch=False)
    parser_load_local.add_argument('archive_file')
    parser_load_local.add_argument('--exist-ok', '-f', action='store_true')
    parser_load_local.add_argument('--export-loose-files', '-l', metavar='target_directory', nargs='?', action='append')

    parser_new = subparsers.add_parser('new', aliases='n')
    parser_new.set_defaults(func=new)
    parser_new.add_argument('source_file_or_directory')
    parser_new.add_argument('--exist-ok', '-f', action='store_true')
    parser_new.add_argument('--export-archive', '-a', metavar='target_file', nargs='?', action='append')
    parser_new.add_argument('--export-signed-archive', '-s', metavar='target_file', nargs='?', action='append')

    args = parser.parse_args()
    args.func(args)


def type_name(obj) -> str:
    return type.__getattribute__(type(obj), '__name__')


@contextmanager
def exc_handler():
    try:
        yield
    except Exception as e:
        exit(f'{parser.prog}: {type_name(e)}: {e}')


@exc_handler()
def load(args: Namespace):
    if args.fetch:
        archive = dlarchive(args.wflow_id)
    else:
        archive = Archive.load_from_path(args.archive_file)
    if args.export_archive:
        archive.export_archive(args.export_archive[-1], exist_ok=args.exist_ok)
    if args.export_signed_archive:
        archive.export_signed_archive(args.export_signed_archive[-1], exist_ok=args.exist_ok)
    if args.export_loose_files:
        archive.export_loose_files(args.export_loose_files[-1], exist_ok=args.exist_ok)


@exc_handler()
def new(args: Namespace):
    archive = Archive.new(args.source_file_or_directory)
    if args.export_archive:
        archive.export_archive(args.export_archive[-1], exist_ok=args.exist_ok)
    if args.export_signed_archive:
        archive.export_signed_archive(args.export_signed_archive[-1], exist_ok=args.exist_ok)
