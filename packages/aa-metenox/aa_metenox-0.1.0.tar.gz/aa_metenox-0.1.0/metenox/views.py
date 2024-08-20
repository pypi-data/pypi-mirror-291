"""Views."""

from django_datatables_view.base_datatable_view import BaseDatatableView

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import format_html
from esi.decorators import token_required

from allianceauth.eveonline.evelinks import dotlan
from allianceauth.eveonline.models import EveCorporationInfo
from app_utils.allianceauth import notify_admins
from app_utils.views import link_html

from .app_settings import METENOX_ADMIN_NOTIFICATIONS_ENABLED
from .models import ESI_SCOPES, HoldingCorporation, Moon, MoonGooPrice, Owner
from .moons import list_all_moons


def add_common_context(context: dict) -> dict:
    """Enhance the templates context with context that should be added to every page"""
    if basic_title := context.get("page_title"):
        context["page_title"] = f"{basic_title} - Metenox"
    else:
        context["page_title"] = "Metenox"

    return context


@login_required
@permission_required("metenox.basic_access")
def index(request):
    """Render index view."""
    moons = list_all_moons()
    return render(request, "metenox/index.html", add_common_context({"moons": moons}))


# pylint: disable = too-many-ancestors
class MoonListJson(PermissionRequiredMixin, LoginRequiredMixin, BaseDatatableView):
    """Datatable view rendering all moons"""

    model = Moon
    permission_required = "metenox.basic_access"
    columns = [
        "id",
        "moon_name",
        "rarity_class_str",
        "solar_system_link",
        "location_html",
        "region_name",
        "constellation_name",
        "value",
        "solar_system_name",
    ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non-sortable columns use empty
    # value like ''
    order_columns = [
        "pk",
        "",
        "",
        "value",
        "",
        "",
        "",
        "",
        "",
    ]

    def render_column(self, row, column):
        if column == "id":
            return row.pk

        if column == "moon_name":
            return row.name

        if result := self._render_location(row, column):
            return result

        return super().render_column(row, column)

    def get_initial_queryset(self):
        return self.initial_queryset()

    @classmethod
    def initial_queryset(cls):
        """Initial query"""
        moon_query = Moon.objects.select_related(
            "eve_moon",
            "eve_moon__eve_planet__eve_solar_system",
            "eve_moon__eve_planet__eve_solar_system__eve_constellation__eve_region",
            "moonmining_moon",
        ).annotate(
            rarity_class_str=Concat(
                Value("R"),
                F("moonmining_moon__rarity_class"),
                output_field=models.CharField(),
            )
        )

        return moon_query

    def filter_queryset(self, qs):
        """Use params in the GET to filter"""
        qs = self._apply_search_filter(
            qs,
            7,
            "eve_moon__eve_planet__eve_solar_system__eve_constellation__eve_region__name",
        )
        qs = self._apply_search_filter(
            qs, 6, "eve_moon__eve_planet__eve_solar_system__eve_constellation__name"
        )
        qs = self._apply_search_filter(
            qs, 4, "eve_moon__eve_planet__eve_solar_system__name"
        )
        qs = self._apply_search_filter(qs, 5, "rarity_class_str")

        if search := self.request.GET.get("search[value]", None):
            qs = qs.filter(eve_moon__name__istartswith=search)
        return qs

    def _apply_search_filter(self, qs, column_num, field) -> models.QuerySet:
        my_filter = self.request.GET.get(f"columns[{column_num}][search][value]", None)
        if my_filter:
            if self.request.GET.get(f"columns[{column_num}][search][regex]", False):
                kwargs = {f"{field}__iregex": my_filter}
            else:
                kwargs = {f"{field}__istartswith": my_filter}
            return qs.filter(**kwargs)
        return qs

    def _render_location(self, row: Moon, column):
        solar_system = row.eve_moon.eve_planet.eve_solar_system
        if solar_system.is_high_sec:
            sec_class = "text-high-sec"
        elif solar_system.is_low_sec:
            sec_class = "text-low-sec"
        else:
            sec_class = "text-null-sec"
        solar_system_link = format_html(
            '{}&nbsp;<span class="{}">{}</span>',
            link_html(dotlan.solar_system_url(solar_system.name), solar_system.name),
            sec_class,
            round(solar_system.security_status, 1),
        )

        constellation = row.eve_moon.eve_planet.eve_solar_system.eve_constellation
        region = constellation.eve_region
        location_html = format_html(
            "{}<br><em>{}</em>", constellation.name, region.name
        )
        if column == "solar_system_name":
            return solar_system.name

        if column == "solar_system_link":
            return solar_system_link

        if column == "location_html":
            return location_html

        if column == "region_name":
            return region.name

        if column == "constellation_name":
            return constellation.name

        return None


@login_required
@permission_required("metenox.basic_access")
def moons_fdd_data(request) -> JsonResponse:
    """Provide lists for drop down fields"""
    qs = MoonListJson.initial_queryset()
    columns = request.GET.get("columns")
    result = {}
    if columns:
        for column in columns.split(","):
            options = _calc_options(request, qs, column)
            result[column] = sorted(list(set(options)), key=str.casefold)
    return JsonResponse(result, safe=False)


# pylint: disable = too-many-return-statements
def _calc_options(request, qs, column):
    if column == "region_name":
        return qs.values_list(
            "eve_moon__eve_planet__eve_solar_system__eve_constellation__eve_region__name",
            flat=True,
        )

    if column == "constellation_name":
        return qs.values_list(
            "eve_moon__eve_planet__eve_solar_system__eve_constellation__name",
            flat=True,
        )

    if column == "solar_system_name":
        return qs.values_list(
            "eve_moon__eve_planet__eve_solar_system__name",
            flat=True,
        )

    if column == "rarity_class_str":
        return qs.values_list("rarity_class_str", flat=True)

    return [f"** ERROR: Invalid column name '{column}' **"]


@permission_required(["moonmining.basic_access"])
@token_required(scopes=ESI_SCOPES)
@login_required
def add_owner(request, token):
    """Render view to add an owner."""
    character_ownership = get_object_or_404(
        request.user.character_ownerships.select_related("character"),
        character__character_id=token.character_id,
    )
    try:
        corporation = EveCorporationInfo.objects.get(
            corporation_id=character_ownership.character.corporation_id
        )
    except EveCorporationInfo.DoesNotExist:
        corporation = EveCorporationInfo.objects.create_corporation(
            corp_id=character_ownership.character.corporation_id
        )
        corporation.save()

    holding_corporation, _ = HoldingCorporation.objects.get_or_create(
        corporation=corporation,
    )

    owner = Owner.objects.update_or_create(
        corporation=holding_corporation,
        defaults={"character_ownership": character_ownership},
    )[0]
    # TODO code update_owner
    # tasks.update_owner.delay(owner.pk)
    messages.success(request, f"Update of refineries started for {owner}.")
    if METENOX_ADMIN_NOTIFICATIONS_ENABLED:
        notify_admins(
            message=f"{owner} was added as new owner by {request.user}.",
            title=f"Metenox: Owner added: {owner}",
        )
    return redirect("metenox:index")


@permission_required(["moonmining.basic_access"])
@login_required
def corporations(request):
    """
    Displays the corporations that the user is allowed to see and the metenoxes that they own
    """

    user_owners = Owner.get_owners_associated_to_user(request.user)
    holdings = [owner.corporation for owner in user_owners]

    metenoxes = {holding: list(holding.metenoxes.all()) for holding in holdings}

    return render(
        request,
        "metenox/corporations.html",
        add_common_context(
            {
                "holding_corporations": holdings,
                "metenoxes": metenoxes,
            }
        ),
    )


@login_required
@permission_required("metenox.basic_access")
def prices(request):
    """Displays moon goo prices"""
    goo_prices = MoonGooPrice.objects.all()

    return render(
        request,
        "metenox/prices.html",
        add_common_context(
            {
                "goo_prices": goo_prices,
            }
        ),
    )
