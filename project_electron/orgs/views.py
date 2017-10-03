# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, UpdateView, CreateView, DetailView, View

from orgs.models import Organization, User
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.messages.views import SuccessMessageMixin

from braces import views

from orgs.models import Archives
from orgs.form import OrgUserUpdateForm, RACSuperUserUpdateForm

from django.contrib import messages
from django.urls import reverse, reverse_lazy

from braces.views import GroupRequiredMixin, StaffuserRequiredMixin, SuperuserRequiredMixin



class LoggedInMixinDefaults(views.LoginRequiredMixin):
    login_url = '/app'

class RACAdminMixin(LoggedInMixinDefaults, SuperuserRequiredMixin):
    authenticated_redirect_url = reverse_lazy(u"app_home")

class RACUserMixin(LoggedInMixinDefaults, StaffuserRequiredMixin):
    authenticated_redirect_url = reverse_lazy(u"app_home")



class OrganizationCreateView(RACAdminMixin, SuccessMessageMixin, CreateView):
    template_name = 'orgs/create.html'
    model = Organization
    fields = ['name']
    success_message = "New Organization Saved!"
    def get_success_url(self):
        return reverse('orgs-detail', kwargs={'pk': self.object.pk})

class OrganizationDetailView(RACUserMixin, DetailView):
    template_name = 'orgs/detail.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        print context
        context['uploads'] = Archives.objects.filter(organization = context['object']).order_by('-pk')
        return context

class OrganizationEditView(RACAdminMixin, SuccessMessageMixin,UpdateView):
    template_name = 'orgs/update.html'
    model =         Organization
    fields =        ['is_active','name']
    success_message = "Organization Saved!"


    def get_success_url(self):
        return reverse('orgs-detail', kwargs={'pk': self.object.pk})

    

class OrganizationListView(RACUserMixin, ListView):

    template_name = 'orgs/list.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class UsersListView(RACUserMixin, ListView):
    template_name = 'orgs/users/list.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()

        refresh_ldap = User.refresh_ldap_accounts()
        if refresh_ldap:
            messages.info(self.request, '{} new accounts were just synced!'.format(refresh_ldap))

        page_title = 'All Users'

        context['users_list'] = [{'org' : {}, 'users' : []}]
        page_type = self.kwargs.get('page_type',None)
        if page_type:
            if page_type == 'company':
                context['users_list'] = Organization.users_by_org()
                page_title = 'Users By Organization'
            elif page_type == 'unassigned':
                context['users_list'][0]['org'] = {'pass':'pass'}
                context['users_list'][0]['users'] = User.objects.filter(from_ldap=True,is_new_account=True,organization=None).order_by('username')
                page_title = 'UnAssigned Users'
        else:
            context['users_list'][0]['org'] = {'pass':'pass'}
            context['users_list'][0]['users'] = User.objects.all().order_by('username')
        context['page_type'] = page_type
        context['page_title'] = page_title

        return context

class UsersDetailView(RACUserMixin, DetailView):
    template_name = 'orgs//users/detail.html'
    model = User

class UsersEditView(RACAdminMixin, SuccessMessageMixin, UpdateView):
    template_name = 'orgs/users/update.html'
    model = User
    success_message = "saved!"

    def get_form_class(self):
        return (RACSuperUserUpdateForm if self.if_editing_staffer() else OrgUserUpdateForm)

    def if_editing_staffer(self):
        return (True if self.object.username[:2] == "va" else False)

    def get_context_data(self, **kwargs):
        context = super(UsersEditView, self).get_context_data(**kwargs)
        context['editing_staffer'] = self.if_editing_staffer()
        return context

    def get_success_url(self):
        return reverse('users-detail', kwargs={'pk': self.object.pk})