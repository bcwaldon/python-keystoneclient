# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.
# Copyright 2011 Nebula, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import getpass
import sys

from keystoneclient.v2_0 import client
from keystoneclient import utils

CLIENT_CLASS = client.Client


@utils.arg('tenant', metavar='<tenant_id>', nargs='?',
           help='ID of Tenant. (Optional)', default=None)
def do_user_list(kc, args):
    """List all users."""
    users = kc.users.list(tenant_id=args.tenant)
    utils.print_list(users, ['id', 'enabled', 'email', 'name', 'tenantId'])


def _getpass():
    """Securely prompt the user for a password"""
    p1 = getpass.getpass('Enter new user password: ')
    p2 = getpass.getpass('Retype new user password: ')
    if p1 == p2:
        return p1
    else:
        print 'Passwords do not match!'
        sys.exit(1)


@utils.arg('--name', metavar='<user-name>', nargs='?',
           help='Desired username. (unique)')
@utils.arg('--pass', metavar='<password>', nargs='?',
           help='Desired password.', dest='passwd')
@utils.arg('--email', metavar='<email>', nargs='?',
           help='Desired email address. (unique)')
@utils.arg('--tenant_id', metavar='<tenant-id>', nargs='?',
           help='User will join the default tenant as a Member.')
@utils.arg('--enabled', metavar='<enabled>', nargs='?', default=True,
           help='Enable user immediately (Optional, default True)')
def do_user_create(kc, args):
    """Create user."""
    if args.passwd is None:
        args.passwd = _getpass()

    user = kc.users.create(args.name, args.passwd, args.email,
                           tenant_id=args.tenant_id, enabled=args.enabled)
    utils.print_dict(user._info)


@utils.arg('--name', metavar='<user-name>', nargs='?',
           help='New desired user name.')
@utils.arg('--email', metavar='<email>', nargs='?',
           help='New desired email address.')
@utils.arg('--enabled', metavar='<email>', nargs='?', default=True,
           help='Enable (true) or Disable (false) user.')
@utils.arg('id', metavar='<user_id>', help='User ID to update.')
def do_user_update(kc, args):
    """Update user's name, email, and enabled status."""
    user = kc.users.update(args.id, name=args.name, email=args.email,
                           enabled=args.enabled)
    utils.print_dict(user._info)


@utils.arg('--pass', metavar='<password>', nargs='?',
           help='New desired password.', dest='passwd')
@utils.arg('id', metavar='<user_id>', help='User ID to update.')
def do_user_password_update(kc, args):
    """Update user password."""
    if args.passwd is None:
        args.passwd = _getpass()
    kc.users.update_password(args.id, args.passwd)


@utils.arg('id', metavar='<user_id>', help='User ID to delete.')
def do_user_delete(kc, args):
    """Delete user."""
    kc.users.delete(args.id)


def do_tenant_list(kc, args):
    """Fetch a list of all tenants."""
    tenants = kc.tenants.list()
    utils.print_list(tenants, ['id', 'name', 'enabled'])


@utils.arg('id', metavar='<tenant_id>', help='Tenant ID to show.')
def do_tenant_get(kc, args):
    """Fetch tenant."""
    tenant = kc.tenants.get(args.id)
    utils.print_dict(tenant._info)


@utils.arg('--name', metavar='<tenant_name>', nargs='?',
           help='Desired name of new tenant.', required=True)
@utils.arg('--description', metavar='<description>', nargs='?', default=None,
           help='Useful description of new tenant (optional, default is None)')
@utils.arg('--enabled', metavar='<True/False>', nargs='?', default=True,
           help='Enable user immediately (Optional, default True)')
def do_tenant_create(kc, args):
    """Create tenant."""
    tenant = kc.tenants.create(args.name,
                             description=args.description,
                             enabled=args.enabled)
    utils.print_dict(tenant._info)


@utils.arg('--name', metavar='<tenant_name>', nargs='?',
           help='Desired name of tenant.')
@utils.arg('--description', metavar='<description>', nargs='?', default=None,
           help='Desired description of tenant')
@utils.arg('--enabled', metavar='<True/False>', nargs='?', const=True,
           help='Enable/disable tenant')
@utils.arg('id', metavar='<tenant_id>', help='Tenant ID to update')
def do_tenant_update(kc, args):
    """Update tenant name, description, enabled status."""
    tenant = kc.tenants.get(args.id)
    kwargs = {}
    if args.name:
        kwargs.update({'name': args.name})
    if args.description:
        kwargs.update({'description': args.description})
    if args.enabled:
        new_enable = args.enabled.lower() in ['true', 'yes', '1']
        kwargs.update({'enabled': new_enable})

    if kwargs == {}:
        print "Tenant not updated, no arguments present."
        return
    tenant.update(**kwargs)


@utils.arg('id', metavar='<tenant_id>', help='Tenant ID to delete')
def do_tenant_delete(kc, args):
    """Delete tenant."""
    kc.tenants.delete(args.id)


@utils.arg('--name', metavar='<name>',
           help='Desired name of service. (unique)', required=True)
@utils.arg('--type', metavar='<type>', required=True,
           help='Possible service types: identity, compute, network, \
                 image, or object-store.')
@utils.arg('--description', metavar='<service_description>', nargs='?',
           help='Useful description of service.')
def do_service_create(kc, args):
    """Add service to Service Catalog."""
    service = kc.services.create(args.name,
                                 args.type,
                                 args.description)
    utils.print_dict(service._info)


def do_service_list(kc, args):
    """List all services in Service Catalog."""
    services = kc.services.list()
    utils.print_list(services, ['id', 'name', 'type', 'description'])


@utils.arg('id', metavar='<service_id>', help='ID of Service to retrieve.')
def do_service_get(kc, args):
    """Fetch service from Service Catalog."""
    service = kc.services.get(args.id)
    utils.print_dict(service._info)


@utils.arg('id', metavar='<service_id>', help='ID of Service to delete')
def do_service_delete(kc, args):
    """Delete service from Service Catalog."""
    kc.services.delete(args.id)


def do_role_list(kc, args):
    """Fetch list of all available roles."""
    roles = kc.roles.list()
    utils.print_list(roles, ['id', 'name'])


@utils.arg('id', metavar='<role_id>', help='ID of Role to fetch.')
def do_role_get(kc, args):
    """Fetch role."""
    role = kc.roles.get(args.id)
    utils.print_dict(role._info)


@utils.arg('--name', metavar='<name>', help='Desired name of new role.')
def do_role_create(kc, args):
    """Create role."""
    role = kc.roles.create(args.name)
    utils.print_dict(role._info)


@utils.arg('id', metavar='<role_id>', help='ID of Role to delete.')
def do_role_delete(kc, args):
    """Delete role."""
    kc.roles.delete(args.id)


# TODO(jakedahn): refactor this to allow role, user, and tenant names.
@utils.arg('--user', metavar='<user_id>', help='ID of User', required=True)
@utils.arg('--role', metavar='<role_id>', help='ID of Role', required=True)
@utils.arg('--tenant_id', metavar='<tenant_id>',
           help='ID of Tenant', nargs='?')
def do_user_add_role(kc, args):
    """Add role to user"""
    kc.roles.add_user_role(args.user, args.role, args.tenant_id)


# TODO(jakedahn): refactor this to allow role, user, and tenant names.
@utils.arg('--user', metavar='<user_id>', help='ID of User', required=True)
@utils.arg('--role', metavar='<role_id>', help='ID of Role', required=True)
@utils.arg('--tenant_id', metavar='<tenant_id>',
           help='ID of Tenant', nargs='?')
def do_user_remove_role(kc, args):
    """Remove role from user."""
    kc.roles.remove_user_role(args.user, args.role, args.tenant_id)


@utils.arg('--tenant_id', metavar='<tenant_id>', help='ID of Tenant',
                          required=True)
@utils.arg('--user', metavar='<user_id>', help='ID of User', required=True)
def do_ec2_create_credentials(kc, args):
    """Create EC2-compatibile credentials for user per tenant."""
    credentials = kc.ec2.create(args.user, args.tenant_id)
    utils.print_dict(credentials._info)


@utils.arg('--user', metavar='<user_id>', help='ID of User')
def do_ec2_credentials_list(kc, args):
    """List out user's EC2-compatibile credentials."""
    credentials = kc.ec2.list(args.user)
    for cred in credentials:
        cred.tenant = kc.tenants.get(cred.tenant_id).name
    utils.print_list(credentials, ['tenant', 'key', 'secret'])


@utils.arg('--user', metavar='<user_id>', help='ID of User')
@utils.arg('--key', metavar='<access_key>', help='Access Key')
def do_ec2_credentials_delete(kc, args):
    """Delete set of EC2-compatibile credentials."""
    kc.ec2.delete(args.user, args.key)


@utils.arg('--service', metavar='<service_type>',
           help='Service type to return', nargs='?', default=None)
def do_catalog(kc, args):
    """List service catalog, possibly filtered by service."""
    endpoints = kc.service_catalog.get_endpoints(service_type=args.service)
    for (service, service_endpoints) in endpoints.iteritems():
        if len(service_endpoints) > 0:
            print "Service: %s" % service
            for ep in service_endpoints:
                utils.print_dict(ep)


@utils.arg('--endpoint_type', metavar='<endpoint_type>',
           help='Endpoint type to select', nargs='?', default='publicURL')
@utils.arg('--service', metavar='<service_type>',
           help='Service type to select', nargs='?', required=True)
@utils.arg('--attr', metavar='<attribute>',
           help='Attribute to match', nargs='?')
@utils.arg('--value', metavar='<value>',
           help='Value of attribute to match', nargs='?')
def do_endpoint_get(kc, args):
    """Find endpoint filtered by a specific attribute or service type."""
    kwargs = {
        'service_type': args.service,
        'endpoint_type': args.endpoint_type,
    }

    if args.attr and args.value:
        kwargs.update({'attr': args.attr, 'filter_value': args.value})
    elif args.attr or args.value:
        print 'Both --attr and --value required.'
        return

    url = kc.service_catalog.url_for(**kwargs)
    utils.print_dict({'%s.%s' % (args.service, args.endpoint_type): url})


def do_token_get(kc, args):
    """Fetch the current user's token."""
    utils.print_dict(kc.service_catalog.get_token())
