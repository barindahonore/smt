from django.contrib import admin
from django.db.models import Count, Avg
from django.db.models.functions import ExtractYear
from django.utils.timezone import now

# from members.models import Child, Reason
# from members.models import MemberProfile
from django.db.models import F, ExpressionWrapper, fields
from datetime import date


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        #
        # Retrieve your custom data
        # available_children_count = Child.objects.count()
        # boys_count = Child.objects.filter(sex="M").count()
        # girls_count = Child.objects.filter(sex="F").count()
        # data_c = MemberProfile.objects.filter(user_type="sector_user").count()

        # most_frequent_reasons = (
        #     Child.objects.values("reasons_to_be_on_the_street__reason_text")
        #     .annotate(count=Count("reasons_to_be_on_the_street__reason_text"))
        #     .order_by("-count")[:5]
        # )

        # region_with_most_children = (
        #     Child.objects.values("current_address")
        #     .annotate(count=Count("current_address"))
        #     .order_by("-count")
        #     .first()
        # )

        # case_study_regions = [
        #     "Region1",
        #     "Region2",
        #     "Region3",
        # ]  # Replace with actual regions
        # children_outside_case_study = Child.objects.exclude(
        #     current_address__in=case_study_regions
        # ).count()

        # today = now().date()
        # current_year = today.year
        # age_expr = ExpressionWrapper(
        #     current_year - ExtractYear("date_of_birth"),
        #     output_field=fields.IntegerField(),
        # )

        # average_age_by_region = (
        #     Child.objects.annotate(age=age_expr)
        #     .values("current_address")
        #     .annotate(average_age=Avg("age"))
        #     .order_by("current_address")
        # )

        extra_context = extra_context or {}
        # extra_context.update(
        #     {
        #         "available_children_count": available_children_count,
        #         "boys_count": boys_count,
        #         "girls_count": girls_count,
        #         "members": data_c,
        #         "most_frequent_reasons": most_frequent_reasons,
        #         "region_with_most_children": region_with_most_children,
        #         "children_outside_case_study": children_outside_case_study,
        #         "average_age_by_region": average_age_by_region,
        #     }
        # )

        # Call the parent index method with the updated extra_context
        return super().index(request, extra_context)


admin.site = CustomAdminSite()
