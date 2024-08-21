"""PvE Views"""

import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.html import format_html
from django.views.decorators.http import require_POST
from esi.decorators import token_required

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCorporationInfo

from assets.models import Owner, Request
from assets.hooks import get_extension_logger, add_info_to_context
from assets.tasks import update_assets_for_owner

logger = get_extension_logger(__name__)


@login_required
@permission_required("assets.basic_access")
def index(request):
    context = {}
    context = add_info_to_context(request, context)
    
    return render(request, "assets/index.html", context=context)


@login_required
@token_required(
    scopes=["esi-universe.read_structures.v1", "esi-assets.read_corporation_assets.v1"]
)
@permission_required("assets.basic_access")
def add_corp(request, token) -> HttpResponse:
    char = get_object_or_404(
        CharacterOwnership, character__character_id=token.character_id
    )
    corp, _ = EveCorporationInfo.objects.get_or_create(
        corporation_id=char.character.corporation_id,
        defaults={
            "member_count": 0,
            "corporation_ticker": char.character.corporation_ticker,
            "corporation_name": char.character.corporation_name,
        },
    )

    owner, _ = Owner.objects.update_or_create(character=char, corporation=corp)
    skip_date = timezone.now() - datetime.timedelta(hours=2)

    if owner.last_update <= skip_date:
        update_assets_for_owner.apply_async(
            args=[owner.pk], kwargs={"force_refresh": True}, priority=6
        )
        msg = f"{owner.name} successfully added/updated to Assets"
        messages.info(request, msg)
        return redirect("assets:index")
    msg = f"{owner.name} is already up to date"
    messages.warning(request, msg)
    return redirect("assets:index")


@login_required
@token_required(scopes=["esi-universe.read_structures.v1", "esi-assets.read_assets.v1"])
@permission_required("assets.basic_access")
def add_char(request, token) -> HttpResponse:
    char = get_object_or_404(
        CharacterOwnership, character__character_id=token.character_id
    )
    owner, _ = Owner.objects.update_or_create(
        corporation=None,
        character=char,
    )
    skip_date = timezone.now() - datetime.timedelta(hours=2)

    if owner.last_update <= skip_date:
        update_assets_for_owner.apply_async(
            args=[owner.pk], kwargs={"force_refresh": True}, priority=6
        )
        msg = f"{owner.name} successfully added/updated to Assets"
        messages.info(request, msg)
        return redirect("assets:index")
    msg = f"{owner.name} is already up to date"
    messages.warning(request, msg)
    return redirect("assets:index")


@login_required
@permission_required("assets.basic_access")
@require_POST
def create_order(request):
    quantities = request.POST.getlist("quantity[]")
    item_names = request.POST.getlist("item_name[]")
    item_ids = request.POST.getlist("item_id[]")
    
    items = []
    msg = ""
    for item_id, name, quantity in zip(item_ids, item_names, quantities):
        if quantity:
            msg += f"{name} - {quantity} Stück\n"
            item_info = {"item_id": item_id, "name": name, "quantity": quantity}
            items.append(item_info)

    # Convert the items list to a JSON string
    items_json = json.dumps(items)

    user = request.user
    user_request = Request.objects.create(
        order=items_json,
        requesting_user=user,
        status=Request.STATUS_OPEN,
    )

    user_request.notify_new_request()
    messages.success(
        request,
        format_html("Your Order has been Requested."),
    )

    return redirect("assets:index")
