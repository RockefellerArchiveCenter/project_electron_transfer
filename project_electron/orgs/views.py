# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, UpdateView, CreateView, DetailView, View
from django.contrib.auth.views import PasswordChangeView

from orgs.models import Organization, User, Archives
from orgs.form import OrgUserUpdateForm, RACSuperUserUpdateForm, UserPasswordChangeForm
from orgs.authmixins import *
from orgs.donorauthmixins import DonorOrgReadAccessMixin

from rights.models import RightsStatement

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.messages.views import SuccessMessageMixin

from orgs.models import Archives, Organization
from orgs.form import OrgUserUpdateForm, RACSuperUserUpdateForm

from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

from orgs.authmixins import *
from orgs.formatmixins import CSVResponseMixin

from orgs.form import UserPasswordChangeForm


class OrganizationCreateView(ManagingArchivistMixin, SuccessMessageMixin, CreateView):
    template_name = 'orgs/create.html'
    model = Organization
    fields = ['name', 'acquisition_type']
    success_message = "New Organization Saved!"

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['meta_page_title'] = 'Add Organization'
        context['acquisition_types'] = Organization.ACQUISITION_TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse('orgs-detail', kwargs={'pk': self.object.pk})

class OrganizationDetailView(DonorOrgReadAccessMixin, DetailView):
    template_name = 'orgs/detail.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context['meta_page_title'] = self.object.name
        context['uploads'] = Archives.objects.filter(process_status__gte=20, organization = context['object']).order_by('-created_time')[:15]
        context['uploads_count'] = Archives.objects.filter(process_status__gte=20, organization = context['object']).count()
        return context

class OrganizationEditView(ManagingArchivistMixin, SuccessMessageMixin, UpdateView):
    template_name = 'orgs/update.html'
    model =         Organization
    fields =        ['is_active','name', 'acquisition_type']
    success_message = "Organization Saved!"

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['meta_page_title'] = 'Edit Organization'
        context['acquisition_types'] = Organization.ACQUISITION_TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse('orgs-detail', kwargs={'pk': self.object.pk})

class OrganizationTransfersView(DonorOrgReadAccessMixin, ListView):
    template_name = 'orgs/all_transfers.html'
    def get_context_data(self,**kwargs):
        context = super(OrganizationTransfersView, self).get_context_data(**kwargs)
        context['organization'] = self.organization
        context['meta_page_title'] = self.organization.name + ' transfers'
        return context

    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'])
        archives = Archives.objects.filter(process_status__gte=20, organization=self.organization).order_by('-created_time')
        for archive in archives:
            archive.bag_info_data = archive.get_bag_data()
        return archives

class OrganizationListView(ArchivistMixin, ListView):

    template_name = 'orgs/list.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['meta_page_title'] = 'Organizations'
        return context

class OrganizationTransferDataView(CSVResponseMixin, DonorOrgReadAccessMixin, View):

    def get(self, request, *args, **kwargs):
        data = [('Bag Name','Status','Size','Upload Time','Errors')]
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'])
        transfers = Archives.objects.filter(process_status__gte=20, organization=self.organization).order_by('-created_time')
        for transfer in transfers:
            transfer_errors = transfer.get_errors()
            errors = (', '.join([e.code.code_desc for e in transfer_errors]) if transfer_errors else '')

            data.append((
                transfer.bag_or_failed_name(),
                transfer.process_status,
                transfer.machine_file_size,
                transfer.machine_file_upload_time,
                errors))
        return self.render_to_csv(data)

class UsersListView(ArchivistMixin, ListView):
    template_name = 'orgs/users/list.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)

        context['meta_page_title'] = 'Users'

        refresh_ldap = User.refresh_ldap_accounts()
        if refresh_ldap:
            messages.info(self.request, '{} new accounts were just synced!'.format(refresh_ldap))

        context['users_list'] = [{'org' : {}, 'users' : []}]
        context['users_list'][0]['org'] = {'pass':'pass'}
        context['users_list'][0]['users'] = User.objects.all().order_by('username')

        context['org_users_list'] = [{'org' : {}, 'users' : []}]
        context['org_users_list'] = Organization.users_by_org()

        context['next_unassigned_user'] = User.objects.filter(from_ldap=True,is_new_account=True,organization=None).order_by('username').first()

        return context

class UsersCreateView(ManagingArchivistMixin, SuccessMessageMixin, CreateView):
    template_name = 'orgs/users/update.html'
    model = User
    fields = ['is_new_account']
    success_message = "New User Saved!"

    def get_form_class(self):
        return (OrgUserUpdateForm)

    def get_success_url(self):
        return reverse('users-detail', kwargs={'pk': self.object.pk})

class UsersDetailView(SelfOrManagerMixin, DetailView):
    template_name = 'orgs/users/detail.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(UsersDetailView, self).get_context_data(**kwargs)
        context['meta_page_title'] = self.object.username
        context['uploads'] = []
        archives = Archives.objects.filter(process_status__gte=20, organization = context['object'].organization).order_by('-created_time')[:5]
        for archive in archives:
            archive.bag_info_data = archive.get_bag_data()
            context['uploads'].append(archive)
        context['uploads_count'] = Archives.objects.filter(process_status__gte=20, organization = context['object'].organization).count()
        return context

class UsersEditView(ManagingArchivistMixin, SuccessMessageMixin, UpdateView):
    template_name = 'orgs/users/update.html'
    model = User
    page_title = "Edit User"
    success_message = "Your changes have been saved!"

    def get_form_class(self):
        return (RACSuperUserUpdateForm if self.if_editing_staffer() else OrgUserUpdateForm)

    def if_editing_staffer(self):
        return (True if self.object.username[:2] == "va" else False)

    def get_context_data(self, **kwargs):
        context = super(UsersEditView, self).get_context_data(**kwargs)
        context['editing_staffer'] = self.if_editing_staffer()
        context['page_title'] = "Edit User"
        context['meta_page_title'] = "Edit User"
        return context

    def get_success_url(self):
        return reverse('users-detail', kwargs={'pk': self.object.pk})

class UsersTransfersView(DonorOrgReadAccessMixin, ListView):
    template_name = 'orgs/all_transfers.html'
    def get_context_data(self,**kwargs):
        context = super(UsersTransfersView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['organization'] = self.user.organization
        context['meta_page_title'] = 'My Transfers'
        return context

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        archives = Archives.objects.filter(user_uploaded=self.user).order_by('-created_time')
        for archive in archives:
            archive.bag_info_data = archive.get_bag_data()
        return archives

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'orgs/users/password_change.html'
    model = User
    success_message = "New password saved."
    form_class = UserPasswordChangeForm

    # def post(self, request, *args, **kwargs):
    #     from django.core.exceptions import ValidationError
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)

    #     try:
    #         if form.is_valid():
    #             return self.form_valid(form)
    #         else:
    #             return self.form_invalid(form)
    #     except ValidationError as e:
    #         print e

    #     return self.form_invalid(form)

    def get_context_data(self,**kwargs):
        context = super(UserPasswordChangeView, self).get_context_data(**kwargs)
        context['meta_page_title'] = 'Change Password'
        return context

    def get_success_url(self):
        return reverse('users-detail', kwargs={'pk': self.request.user.pk})
