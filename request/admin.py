from pyexpat import model
from django.contrib import admin
from .models import WithdrawRequest, DepositRequest
from django.contrib import messages
# Register your models here.

@admin.register(WithdrawRequest)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = [ "tx_id", "payment_id" ]
    list_display = ["id", "user", "currency", "amount", "coin_amount", "address", "memo", ]


    def render_change_form(self, request, context, *args, **kwargs):
        """We need to update the context to show the button."""
        # if self.status.find("pending") > -1 :
        if kwargs['obj'] and kwargs['obj'].status.find("pending") > -1 :
            context.update({'confirm_payout': True})
        return super().render_change_form(request, context, *args, **kwargs)


    def response_post_save_change(self, request, obj):
        """This method is called by `self.changeform_view()` when the form
        was submitted successfully and should return an HttpResponse.
        """
        # Check that you clicked the button `_save_and_copy`
        if 'confirm_payout' in request.POST:
            result = obj.confirm(request)
            messages.add_message(request, messages.WARNING,  result)

       


        return super().response_post_save_change(request, obj)

@admin.register(DepositRequest)
class RequestAdmin2(admin.ModelAdmin):
    
    readonly_fields = [ "tx_id", "payment_id" ]
    list_display = ["id", "user", "currency", "amount",  "url" ]
    
