"""
Main entrypoint for builder.
"""

import sys
import warnings
from collections.abc import Iterable, Sequence

from botocore.session import Session as BotocoreSession

from mypy_boto3_builder.cli_parser import CLINamespace, parse_args
from mypy_boto3_builder.enums.product import Product, ProductLibrary
from mypy_boto3_builder.generators.aioboto3_generator import AioBoto3Generator
from mypy_boto3_builder.generators.aiobotocore_generator import AioBotocoreGenerator
from mypy_boto3_builder.generators.base_generator import BaseGenerator
from mypy_boto3_builder.generators.boto3_generator import Boto3Generator
from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.service_name import ServiceName, ServiceNameCatalog
from mypy_boto3_builder.utils.boto3_utils import get_boto3_session, get_botocore_session
from mypy_boto3_builder.utils.botocore_changelog import BotocoreChangelog
from mypy_boto3_builder.utils.strings import get_botocore_class_name
from mypy_boto3_builder.utils.version import get_botocore_version


def get_selected_service_names(
    selected: Iterable[str],
    available: Iterable[ServiceName],
) -> list[ServiceName]:
    """
    Get a list of selected service names.

    Supports `updated` to select only services updated in currect `boto3` release.
    Supports `all` to select all available service names.

    Arguments:
        selected -- Selected service names as strings.
        available -- All ServiceNames available in current boto3 release.

    Returns:
        A list of selected ServiceNames.
    """
    logger = get_logger()
    available_map = {i.name: i for i in available}
    result: list[ServiceName] = []
    selected_service_names = list(selected)
    botocore_version = get_botocore_version()
    if ServiceName.ALL in selected_service_names:
        return list(available)
    if ServiceName.UPDATED in selected_service_names:
        selected_service_names.remove(ServiceName.UPDATED)
        updated_service_names = BotocoreChangelog().fetch_updated(botocore_version)
        for updated_service_name in updated_service_names:
            if updated_service_name in available_map:
                selected_service_names.append(updated_service_name)

    for service_name_str in selected_service_names:
        if service_name_str not in available_map:
            logger.info(f"Service {service_name_str} is not provided by botocore, skipping")
            continue
        result.append(available_map[service_name_str])

    return result


def get_available_service_names(session: BotocoreSession) -> list[ServiceName]:
    """
    Get a list of boto3 supported service names.

    Arguments:
        session -- Boto3 session

    Returns:
        A list of supported services.
    """
    available_services = session.get_available_services()
    result: list[ServiceName] = []
    for name in available_services:
        service_data = session.get_service_data(name)
        metadata = service_data["metadata"]
        class_name = get_botocore_class_name(metadata)
        service_name = ServiceNameCatalog.add(name, class_name)
        result.append(service_name)
    return result


def get_generator_cls(product: Product) -> type[BaseGenerator]:
    """
    Get Generator class for a product.

    Raises:
        ValueError -- If product is not supported.
    """
    library = product.get_library()
    if library == ProductLibrary.boto3:
        return Boto3Generator
    if library == ProductLibrary.aiobotocore:
        return AioBotocoreGenerator
    if library == ProductLibrary.aioboto3:
        return AioBoto3Generator
    raise ValueError(f"Unknown product library: {library}")


def generate_product(
    product: Product,
    args: CLINamespace,
    service_names: Sequence[ServiceName],
    master_service_names: Sequence[ServiceName],
) -> None:
    """
    Generate a selected product.

    Arguments:
        product -- Product to generate
        args -- CLI namespace
        service_names -- Selected service names
        master_service_names -- Service names included in master
    """
    generator_cls = get_generator_cls(product)
    generator = generator_cls(
        service_names=service_names,
        master_service_names=master_service_names,
        output_path=args.output_path,
        generate_setup=not args.installed,
        skip_published=args.skip_published,
        disable_smart_version=args.disable_smart_version,
        version=args.build_version,
        cleanup=True,
    )
    generator.generate_product(product.get_type())


def run(args: CLINamespace) -> None:
    """
    Run builder.
    """
    # FIXME: suppress botocore endpoint warning
    warnings.filterwarnings("ignore", category=FutureWarning, module="botocore.client")

    logger = get_logger(level=args.log_level)

    session = get_boto3_session()

    args.output_path.mkdir(exist_ok=True, parents=True)
    available_service_names = get_available_service_names(get_botocore_session(session))

    logger.info(f"{len(available_service_names)} supported boto3 services discovered")
    if args.list_services:
        for service_name in available_service_names:
            print(
                f"- {service_name.name} : {service_name.class_name} {service_name.boto3_doc_link}"
            )
        return

    service_names = get_selected_service_names(args.service_names, available_service_names)
    master_service_names = service_names if args.partial_overload else available_service_names

    for product in args.products:
        logger.info(f"Generating {product} product")
        generate_product(product, args, service_names, master_service_names)

    logger.info("Completed")


def main() -> None:
    """
    CLI entrypoint.
    """
    args = parse_args(sys.argv[1:])
    run(args)


if __name__ == "__main__":
    main()
