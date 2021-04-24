from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

try:
    from ..core.models import Tag, Ingredient, Recipe
except ImportError:
    from core.models import Tag, Ingredient, Recipe
from . import serializer

# Create your views here.


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializer.TagSerializer


class IngredientViewSets(BaseRecipeAttrViewSet):
    """Manage ingredients in db"""
    queryset = Ingredient.objects.all()
    serializer_class = serializer.IngredientSerializer

# the above three calss is same as below two class
# we are just reducing the repitation of codes
# As the below two class perform same thing
# it can be reduced with a new class i.e. "BseRecipeAttrViewSet" class


# class TagViewSet(viewsets.GenericViewSet,
#                  mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializer.TagSerializer

#     def get_queryset(self):
#         """Return objects for the current authnticates user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         """Create a new tag"""
#         serializer.save(user=self.request.user)


# class IngredientViewSets(viewsets.GenericViewSet,
#                          mixins.ListModelMixin,
#                          mixins.CreateModelMixin):
#     """Manage ingredients in db"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializer.IngredientSerializer

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in DB"""
    serializer_class = serializer.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
