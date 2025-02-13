"""
Sample script to get current Duo Security deployment status
"""
# Built-in imports
from __future__ import annotations, absolute_import
from functools import singledispatchmethod
import argparse
import logging

# Third party imports
import httpx

# Constants
STATUS_URL = 'https://status.duo.com/api/v2/components.json'

logging.basicConfig(
        level=logging.INFO,
        filename='duo_deployment_status.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DuoStatusComponent:
    """Data class for individual Duo Security deployment status components"""

    id: str | None = None
    name: str | None = None
    status: str | None = None
    components: list[str] | None = None

    @singledispatchmethod
    def __init__(self, attrs):
        raise NotImplementedError(f"Unrecognized type {type(attrs)!r}")

    @__init__.register
    def _(self, attrs: dict):
        for key, value in attrs.items():
            setattr(self, key, value)

    @__init__.register
    def _(self, attrs: list):
        logging.info("Creating Duo Security status component using list")
        for attr in attrs:
            if '=' in attr:
                key, value = attr.split('=')
                setattr(self, key, value)


def get_arguments() -> argparse.Namespace:
    """Collect command line arguments."""
    parser = argparse.ArgumentParser(description="Get Duo Deployment status")
    parser.add_argument(
            "duo_deployment_id",
            help="Duo Deployment ID. Example: DUO63")
    return parser.parse_args()


def get_status_components() -> list[DuoStatusComponent]:
    """Connect to the Duo status website and collect current Duo Security deployment statuses"""
    status_components = []
    try:
        json_resp = httpx.get(STATUS_URL).json()

        if 'components' in json_resp:
            for status_component in json_resp['components']:
                status_components.append(DuoStatusComponent(status_component))
        logging.info("Collected %s components", len(status_components))

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")

    return status_components



def extract_components(status_components: list[DuoStatusComponent], deployment_id: str) -> list[DuoStatusComponent]:
    """Retrieve component objects matching deployment ID"""
    if not status_components or not deployment_id:
        raise ValueError("Required arguments missing.")

    if len(status_components) == 0:
        return []

    logging.info("Extracting components for '%s'", deployment_id)

    component_matches = []
    component_group = []

    for status_component in status_components:
        if isinstance(status_component, DuoStatusComponent):
            if status_component.name == deployment_id:
                logging.info("   Found match for %s", status_component.name)
                component_matches.append(status_component)
                component_group = status_component.components
                logging.info("  component_group: %s", component_group)

    if len(component_group) > 0:
        for status_component in status_components:
            if isinstance(status_component, DuoStatusComponent):
                if status_component.id in component_group:
                    logging.info("Found match for %s", status_component.id)
                    component_matches.append(status_component)
    logging.info("Found %s components matching '%s'", len(component_matches), deployment_id)
    return component_matches


if __name__ == '__main__':
    args = get_arguments()
    duo_deployment_id = args.duo_deployment_id.upper()

    logging.info('Duo Deployment ID: %s', duo_deployment_id)

    component_list = extract_components(get_status_components(), duo_deployment_id)

    if len(component_list) > 0:
        for component in component_list:
            print(f"{component.name} status: {component.status}")
