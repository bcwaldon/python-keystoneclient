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

from keystoneclient.v2_0 import client
from keystoneclient import utils

CLIENT_CLASS = client.Client


@utils.arg('tenant',
           metavar='<tenant_id>',
           help='ID of Tenant. (Optional)',
           nargs='?',
           default=None)
def do_user_list(kc, args):
    users = kc.users.list(tenant_id=args.tenant)
    utils.print_list(users, ['id', 'enabled', 'email', 'name', 'tenantId'])


@utils.arg('--name', metavar='<name>', nargs='?',
           help='Desired username. (unique)')
@utils.arg('--pass', metavar='<pass>', nargs='?',
           dest='passwd',
           help='Desired password.')
@utils.arg('--email', metavar='<email>', nargs='?',
           help='Desired email address. (unique)')
@utils.arg('--default-tenant', metavar='<default_tenant>', nargs='?',
           help='User will join the default tenant as a Member.')
@utils.arg('--enabled', metavar='<enabled>', nargs='?', default=True,
           help='Enable user immediately (Optional, default True)')
def do_user_create(kc, args):
    user = kc.users.create(args.name, args.passwd, args.email,
                           tenant_id=args.default_tenant, enabled=args.enabled)
    utils.print_dict(user._info)


@utils.arg('id', metavar='<user_id>', help='User ID to update.')
@utils.arg('--name', metavar='<name>', nargs='?',
           help='Desired user name.')
@utils.arg('--email', metavar='<email>', nargs='?',
           help='Desired email address.')
@utils.arg('--enabled', metavar='<enabled>', nargs='?',
           help='Desired status of tenant.')
def do_user_update(kc, args):
    kwargs = {}
    if args.name:
        kwargs['name'] = args.name
    if args.email:
        kwargs['email'] = args.email
    if args.enabled:
        kwargs['enabled'] = utils.string_to_bool(args.enabled)

    if not len(kwargs):
        print "User not updated, no arguemnts present."
        return

    try:
        kc.users.update(args.id, **kwargs)
    except Exception, e:
        print 'Unable to update user: %s' % e


@utils.arg('id', metavar='<user_id>', nargs='?', help='User ID to update.')
@utils.arg('password', metavar='<password>', nargs='?',
           help='New desired password.')
def do_user_update_password(kc, args):
    try:
        kc.users.update_password(args.id, args.password)
        print 'User password has been udpated.'
    except:
        'Unable to update users password.'


@utils.arg('id', metavar='<user_id>', nargs='?', help='User ID to delete.')
def do_user_delete(kc, args):
    try:
        kc.users.delete(args.id)
        print 'User has been deleted.'
    except:
        'Unable to delete user.'


@utils.arg('--name', metavar='<name>', nargs='?',
           help='Desired name of new tenant.')
@utils.arg('--description', metavar='<description>', nargs='?', default=None,
           help='Useful description of new tenant (optional, default is None)')
@utils.arg('--enabled', metavar='<enabled>', nargs='?', default=True,
           help='Enable user immediately (Optional, default True)')
def do_tenant_create(kc, args):
    tenant = kc.tenants.create(args.name,
                             description=args.description,
                             enabled=args.enabled)
    utils.print_dict(tenant._info)


@utils.arg('id', metavar='<tenant_id>', nargs='?', help='Tenant ID to enable.')
def do_tenant_enable(kc, args):
    try:
        kc.tenants.update(args.id, enabled=True)
        print 'Tenant has been enabled.'
    except:
        'Unable to enable tenant.'


@utils.arg('id', metavar='<tenant_id>', nargs='?', help='Tenant ID to disable')
def do_tenant_disable(kc, args):
    try:
        kc.tenants.update_enabled(args.id, enabled=False)
        print 'Tenant has been disabled.'
    except:
        'Unable to disable tenant.'


@utils.arg('id', metavar='<tenant_id>', nargs='?', help='Tenant ID to delete')
def do_tenant_delete(kc, args):
    try:
        kc.tenants.delete(args.id)
        print 'Tenant has been deleted.'
    except:
        'Unable to delete tenant.'


@utils.arg('--name', metavar='<name>', nargs='?',
           help='Desired name of service. (unique)')
@utils.arg('--type', metavar='<type>', nargs='?',
           help='Possible service types: identity, compute, network, \
                 image, or object-store.')
@utils.arg('--description', metavar='<service_description>', nargs='?',
           help='Useful description of service.')
def do_service_create(kc, args):
    service = kc.services.create(args.name,
                                 args.type,
                                 args.description)
    utils.print_dict(service._info)


def do_service_list(kc, args):
    services = kc.services.list()
    utils.print_list(services, ['id', 'name', 'type', 'description'])


@utils.arg('id',
           metavar='<service_id>',
           help='ID of Service to retrieve.',
           nargs='?')
def do_service_get(kc, args):
    service = kc.services.get(args.id)
    utils.print_dict(service._info)


@utils.arg('id',
           metavar='<service_id>',
           help='ID of Service to delete',
           nargs='?')
def do_service_delete(kc, args):
    try:
        kc.services.delete(args.id)
        print 'Service has been deleted'
    except:
        print 'Unable to delete service.'


def do_role_list(kc, args):
    roles = kc.roles.list()
    utils.print_list(roles, ['id', 'name'])


@utils.arg('id', metavar='<role_id>', help='ID of Role to fetch.', nargs='?')
def do_role_get(kc, args):
    role = kc.roles.get(args.id)
    utils.print_dict(role._info)


@utils.arg('--name', metavar='<name>', nargs='?',
           help='Desired name of new role.')
def do_role_create(kc, args):
    role = kc.roles.create(args.name)
    utils.print_dict(role._info)


@utils.arg('id', metavar='<role_id>', help='ID of Role to delete.', nargs='?')
def do_role_delete(kc, args):
    try:
        kc.roles.delete(args.id)
        print 'Role has been deleted.'
    except:
        print 'Unable to delete role.'


# TODO(jakedahn): refactor this to allow role, user, and tenant names.
@utils.arg('user_id', metavar='<user_id>', help='ID of User', nargs='?')
@utils.arg('role_id', metavar='<role_id>', help='ID of Role', nargs='?')
@utils.arg('tenant_id', metavar='<tenant_id>', help='ID of Tenant', nargs='?')
def do_add_user_role(kc, args):
    kc.roles.add_user_role(args.user_id, args.role_id, args.tenant_id)


# TODO(jakedahn): refactor this to allow role, user, and tenant names.
@utils.arg('user_id', metavar='<user_id>', help='ID of User', nargs='?')
@utils.arg('role_id', metavar='<role_id>', help='ID of Role', nargs='?')
@utils.arg('tenant_id', metavar='<tenant_id>', help='ID of Tenant', nargs='?')
def do_remove_user_role(kc, args):
    kc.roles.remove_user_role(args.user_id, args.role_id, args.tenant_id)


@utils.arg('--tenant_id', metavar='<tenant_id>', help='ID of Tenant',
           nargs='?')
@utils.arg('--user_id', metavar='<user_id>', help='ID of User', nargs='?')
def do_ec2_create_credentials(kc, args):
    credentials = kc.ec2.create(args.user_id, args.tenant_id)
    utils.print_dict(credentials._info)


@utils.arg('user_id', metavar='<user_id>', help='ID of User', nargs='?')
def do_ec2_list_credentials(kc, args):
    credentials = kc.ec2.list(args.user_id)
    for cred in credentials:
        cred.tenant = kc.tenants.get(cred.tenant_id).name
    utils.print_list(credentials, ['tenant', 'key', 'secret'])


@utils.arg('user_id', metavar='<user_id>', help='ID of User', nargs='?')
@utils.arg('key', metavar='<access_key>', help='Access Key', nargs='?')
def do_ec2_delete_credentials(kc, args):
    try:
        kc.ec2.delete(args.user_id, args.key)
        print 'Deleted EC2 Credentials.'
    except:
        print 'Unable to delete EC2 Credentials.'


@utils.arg('--service', metavar='<service_type>',
        help='Service type to return', nargs='?', default=None)
def do_catalog(kc, args):
    """List service catalog, possibly filtered by service"""
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
    """Find endpoint filtered by a specific attribute or service type"""
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


def do_token(kc, args):
    """Fetch the current user's token"""
    utils.print_dict(kc.service_catalog.get_token())
