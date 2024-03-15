# Third-party
import factory
from user.models import Organization, User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda x: f"fake-email-{x}@fake-domain.com")
    email = factory.Sequence(lambda x: f"fake-email-{x}@fake-domain.com")
    password = factory.Sequence(lambda x: f"Str0ngP4ssw0rd!{x}")
    first_name = factory.Sequence(lambda x: f"Firstname{x}")
    last_name = factory.Sequence(lambda x: f"Lastname{x}")

    class Meta:
        model = User


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
